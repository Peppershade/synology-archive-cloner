# synology-archive-cloner

```
version: '3'
services:
  synology-archiver:
    image: peppershade/synology-archiver:latest
    volumes:
      - /volume1/archive/synology:/app/output
    environment:
      #- model=ds720+
      #- dryrun=true
      - version=6.2
    restart: no
```
Uncomment or comment options when needed, do not leave empty, just comment them

Docker image will stop when finished, check the logs
