FROM node:20.10.0-slim AS build

# Tini
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# Deps
WORKDIR /opt/odf
COPY . .
RUN npm ci
RUN npm run build
RUN npm ci --omit=dev

#########################################################################################

FROM node:20.10.0-slim

COPY --from=build /usr/bin/tini /usr/bin/tini

WORKDIR /opt/odf
COPY --from=build /opt/odf/dist /opt/odf/dist
COPY --from=build /opt/odf/node_modules /opt/odf/node_modules

ENV NODE_ENV production

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["node", "dist/app.js"]
