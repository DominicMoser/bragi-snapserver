FROM alpine:3.21

RUN apk update
RUN apk add snapcast-server
RUN apk add python3 py3-websockets
EXPOSE 1704
EXPOSE 1705
EXPOSE 1780

COPY wsProxyControlScript.py /usr/share/snapserver/plug-ins
RUN chmod +x /usr/share/snapserver/plug-ins

CMD ["snapserver"]
