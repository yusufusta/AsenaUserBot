# Faster & Secure & Special Container #
# Thanks to mkaraniya & zakaryan2004

FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/quiec/AsenaUserBot /root/AsenaUserBot
WORKDIR /root/AsenaUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
