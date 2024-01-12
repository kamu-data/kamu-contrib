version: 1
kind: DatasetSnapshot
content:
  name: testing.set-transform-input-by-id
  kind: Derivative
  metadata:
    - kind: SetTransform
      inputs:
        - datasetRef: "did:odf:<substitiute>"
          alias: foo
      transform:
        kind: Sql
        engine: flink
        query: "select event_time from foo"
