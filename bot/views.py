from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
import json
from bot import answer

 
@csrf_exempt 
def keyboard(request):
    #Parse json and return answer
    try:
        json_str=((request.body).decode('utf-8'))
        data = json.loads(json_str)['userRequest']
        message = data['utterance']
        print(message)
        ans = answer.answer(message)
        print(ans)
    except Exception as e:
        print(e)
        return JsonResponse({
            "version":"2.0",
            "template":{
                "outputs": [
                    {   
                    "simpleText":{
                        "text":"서버 오류"
                    }
                }   
                ]
            }
        })

    return JsonResponse({
        "version":"2.0",
        "template":{
            "outputs": [
            {
                "simpleText":{
                    "text": ans
                }
            }
            ]
        }
    })
