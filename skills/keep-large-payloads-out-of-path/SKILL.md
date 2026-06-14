# Keep Large Payloads Out Of The Request Path

Keep large binaries and blobs off your application servers: store them in a dedicated object store and move them directly between client and store by reference (a pre-signed or direct URL), persisting only a pointer plus metadata in your database. This keeps the unavoidable large transfer on the most efficient path and stops application servers from becoming bandwidth-bound.

## When To Use

- A request carries or returns a large opaque payload (file upload/download, image, video, document, attachment, archive, exported dump).
- Payload size is large or unbounded relative to the structured data the request also touches.
- Application servers (or the API tier) would otherwise read the full payload into memory or stream it through to satisfy the request.
- The payload is content to be stored and later retrieved whole, not data the application must parse, index, or query field-by-field.

## When Not To Use

- The payload is small and bounded (fits comfortably in a normal request/row) and the indirection cost outweighs the benefit.
- The application must inspect, transform, or validate the bytes in-band before they are durably stored, and that processing cannot move to an asynchronous worker after the upload lands.
- A regulatory or trust boundary forbids the client from talking to the store directly and no signed-URL or gateway equivalent is permitted.
- The payload is structured data that needs to be queried/aggregated; that belongs in a queryable store, not an opaque blob.

## Preconditions

- An object store (or equivalent blob storage) reachable by the client, supporting access-scoped references. *(Example: S3 with pre-signed URLs.)*
- A metadata/relational store for the structured record that will hold the pointer and attributes.
- A mechanism to mint short-lived, least-privilege access references (signed URLs or equivalent tokens) scoped to a single object and operation.
- A naming/keying scheme for objects so each blob has a stable identifier referenced from metadata.

## Order Of Operations

1. **Separate the payload from the metadata.** Identify the large opaque part of the request and the small structured part. Only the structured part flows through application services.
2. **Mint a scoped reference.** When a client needs to upload or download, the application server returns a short-lived signed/direct URL scoped to one object and one operation — it does not proxy the bytes.
3. **Transfer client ↔ store directly.** The client uploads to or downloads from the object store using that reference. The bytes never traverse the application tier.
4. **Persist a pointer, not the payload.** Store the object key/locator plus metadata (size, content type, owner, checksum, status) in the database. Never inline the blob contents into a metadata column or message.
5. **Confirm and finalize.** On upload, the application records the object as present (via callback, completion event, or a verification read) and marks the metadata record ready; do any heavy processing asynchronously off the request path.
6. **Reference by pointer everywhere downstream.** Links, notifications, and inter-service messages carry the pointer/URL, not the embedded blob.

## Test Checklist

- [ ] No application/API service reads the full large payload into memory or streams it through to fulfill a request.
- [ ] The database stores a pointer and metadata, not the blob bytes inline.
- [ ] Client-to-store transfer uses a direct/signed reference scoped to one object and operation, with a short expiry.
- [ ] Messages, links, and notifications carry the pointer, not the embedded payload.
- [ ] Per-request work on the application tier is bounded by metadata size, independent of payload size.
- [ ] Heavy processing of payload bytes, if any, runs asynchronously after the object lands, not in the request path.

## Anti-Patterns

- Streaming large blobs through application services, making the app tier bandwidth-bound at scale.
- Storing large content inline in the metadata database instead of a pointer to the object store.
- Sending big attachments inline (in the request body or a message) instead of linking them by reference.
- Issuing long-lived or broadly scoped access references where a short-lived single-object reference suffices.
- Proxying download bytes back through the application server when a direct reference to the store would do.

## Provenance

MP8 — observed in 3 of 8 build-set videos.
