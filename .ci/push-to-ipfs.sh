#!/bin/bash
set -e

AWS_ROUTE53_HOSTED_ZONE_ID=Z25CPWZR4S9IHS
AWS_ROUTE53_TTL=60


dataset_name="$1"
dnslink_subdomain="${dataset_name}.ipns.kamu.dev"

ipfs_cid_old=$( \
    aws route53 list-resource-record-sets --hosted-zone-id $AWS_ROUTE53_HOSTED_ZONE_ID \
    | jq -r ".ResourceRecordSets[] | select(.Name == \"_dnslink.${dnslink_subdomain}.\") | .ResourceRecords[0].Value" \
    | grep -oE '[^/]+"$' \
    | grep -oE '^[^"]+'
)

ipfs_cid=$(kamu system ipfs add ${dataset_name})

if [ "$ipfs_cid_old" == "$ipfs_cid" ]; then
    echo "CID didn't change - skipping publishing"
    exit 0
fi

# Pin new CID to replicate data to the pinning service
for i in $(seq 1 $PIN_TRIES); do
    echo "Pinning CID (attempt $i)"

    if curl --fail -sS -X POST -u "$INFURA_IPFS_DATASETS_PROJECT_ID:$INFURA_IPFS_DATASETS_PROJECT_SECRET" "https://ipfs.infura.io:5001/api/v0/pin/add?arg=$ipfs_cid"; then
        echo "Successfully pinned"
        break
    else
    echo "Pinning service returned an error: $response"

    # TODO: Remove this debug stuff when pinning is reliable
    peers_num=$(ipfs swarm peers | wc -l)
    echo "IPFS is connected to $peers_num peers"

    echo "IPFS addresses:"
    ipfs id

    if curl -s --fail "https://dweb.link/ipfs/${ipfs_cid}" > /dev/null; then
        echo "CID is RESOLVABLE via public gateway"
    else
        echo "CID is NOT resolvable via public gateway"
    fi

    if [ $i == $PIN_TRIES ]; then
        echo "Failed to pin CID after $PIN_TRIES attempts"
        exit 1
    fi
  fi
done

# Update DNSLink entry
echo "{
    \"Comment\": \"GHAction update of DNSLink record\",
    \"Changes\": [
        {
            \"Action\": \"UPSERT\",
            \"ResourceRecordSet\": {
                \"Name\": \"_dnslink.${dnslink_subdomain}.\",
                \"Type\": \"TXT\",
                \"TTL\": ${AWS_ROUTE53_TTL},
                \"ResourceRecords\": [{
                    \"Value\": \"\\\"dnslink=/ipfs/${ipfs_cid}\\\"\"
                }]
            }
        }
    ]
}" > dns-upsert.json

echo "Updating DNSLink entry with: $(cat dns-upsert.json)"
aws --no-cli-pager route53 change-resource-record-sets --hosted-zone-id $AWS_ROUTE53_HOSTED_ZONE_ID --change-batch file://dns-upsert.json
rm dns-upsert.json

echo "Dataset ${dataset_name} successfully pinned as ${ipfs_cid}"
