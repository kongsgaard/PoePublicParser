FROM python:3.8
ADD ./PublichStashApiParser /PublichStashApiParser
WORKDIR /PublichStashApiParser
RUN pip install -r requierments.txt
CMD ["python", "main.py"]