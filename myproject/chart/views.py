from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse

# Create your views here.
from collections import Counter
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

def graphic(request):

        

        
       
        #send reques to
        a=requests.get('https://asia-east2-greentoad-bfbb7.cloudfunctions.net/apiIndia/api/angular')
        b=json.loads(a.text)

        #fatch delay data
        delay_data=[i['delay'] for i in b]
        delay_data=list(dict.fromkeys(delay_data))
        delay_data.pop(0)

        #fatch trip start time
        date_time=[i['trip_start_time'] for i in b]


        month=[] #collect month from trip_start_time

        #split all date time and collect only month
        for i in date_time:
        
            c=i.split(":")
            
            d=c[0]
            
            e=d.split("-")
        
            f=e[1]
            
            month.append(f)
            
        x=month[0:116]
        x.sort()


        #plot bar chart
        plt.bar(x,delay_data , color='red')
        plt.title('delay report')
        plt.xlabel('month')
        plt.ylabel('delay')
        

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')



        
       


        #top 3 source
        source=[i['srcname'] for i in b]
        lst=source
        c = Counter(lst)

        high = c.most_common(3)
        
        print(high)
        #top 3 destination
        Destination=[i['destname'] for i in b]
        lst1=Destination
        d = Counter(lst1)

        high1 = d.most_common(3) 
        print("Top 3 destination are:") 
        print(high1)

        return render(request, 'graphic.html',{'graphic':graphic},{'high':high})
        


