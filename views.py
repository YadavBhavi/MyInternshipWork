from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Org, Suborg, Invitees
from .serializer import OrgSerializer, SuborgSerializer, InviteesSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from datetime import date
from mapi.settings import BASE_URL, BASE_URL_2

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from users.check_permissions import check_permission, check_role, check_multiple_permissions
import jwt
import logging
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions( allowed_permission={'GET': 'get_org_detail', 'PUT': 'update_org_detail', 'DELETE': 'delete_org'})
def org_detail(request, org_id):
    try:
        org = Org.objects.get(pk=org_id)
    except Org.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        try:
            serializer = OrgSerializer(org)
            return JsonResponse(serializer.data)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting org detail"}
            return JsonResponse(response, status=400)

    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
            # logger.error('User %s', data)
            serializer = OrgSerializer(org, data=data)
            # data['created_by_id'] = request.user.id
            if serializer.is_valid():
                serializer.update(org, data)
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while updating org detail"}
            return JsonResponse(response, status=400)

    elif request.method == 'DELETE':
        try:
            org.delete()
            return JsonResponse({'deleted': True}, status=200)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while deleting org "}
            return JsonResponse(response, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions( allowed_permission={'GET': 'get_suborg_detail', 'PUT': 'update_suborg_detail', 'DELETE': 'delete_suborg'})
def suborg_detail(request, org_id, suborg_id):
    try:
        suborg = Suborg.objects.get(pk=suborg_id)
    except Suborg.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        try:
            serializer = SuborgSerializer(suborg)
            return JsonResponse(serializer.data)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting sub org "}
            return JsonResponse(response, status=400)

    elif request.method == 'PUT':

        try:
            data = JSONParser().parse(request)
            # logger.error('User %s', data)
            serializer = SuborgSerializer(suborg, data=data)
            if serializer.is_valid():
                serializer.update(suborg, data)
                return JsonResponse(serializer.data)
            # return JsonResponse(serializer.errors, status=400)

        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while updating sub org "}
            return JsonResponse(response, status=400)

    elif request.method == 'DELETE':
        try:
            suborg.delete()
            return JsonResponse({'deleted': True}, status=200)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while deleting sub org "}
            return JsonResponse(response, status=400)


@csrf_exempt
@swagger_auto_schema(methods=['POST'], request_body=OrgSerializer)
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions( allowed_permission={'GET': 'view_org_list', 'POST': 'add_org_to_org_list'})
def org_list(request):
    if request.method == 'GET':
        try:
            org = Org.objects.all()
            serializer = OrgSerializer(org, many=True)
            return JsonResponse(serializer.data, safe=False)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting the Org details"}
            return JsonResponse(response, status=400)

    elif request.method == 'POST':

        try:
            data = JSONParser().parse(request)
            data['created_by_id'] = request.user.id
            serializer = OrgSerializer(data=data)
            # logger.error('User %s', request.user)
            if serializer.is_valid():
                try:
                    serializer.save()
                except Exception as e:
                    logger.error('User %s', e)
                    return JsonResponse(str(e.message), status=400, safe=False)
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while adding the Org details"}
            return JsonResponse(response, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions( allowed_permission={'GET': 'view_suborg_list', 'POST': 'add_suborg_to_suborg_list'})
def suborg_list(request, org_id):
    if request.method == 'GET':
        try:
            suborg = Suborg.objects.filter(org_reference_id=org_id)
            serializer = SuborgSerializer(suborg, many=True)
            return JsonResponse(serializer.data, safe=False)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting the Sub Org details"}
            return JsonResponse(response, status=400)
    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            data['created_by_id'] = request.user.id
            data['org_reference_id'] = org_id
            serializer = SuborgSerializer(data=data)
            # logger.error('User %s', request.user)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while adding the Sub Org details"}
            return JsonResponse(response, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions(allowed_permission={'GET': 'get_invitees_detail', 'PUT': 'get_invitees_detail', 'DELETE': 'get_invitees_detail'})
def invitees_detail(request, org_id, suborg_id, invitees_id):
    try:
        invitees = Invitees.objects.get(pk=invitees_id)
    except Org.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        try:
            serializer = InviteesSerializer(invitees)
            return JsonResponse(serializer.data)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting invitees details"}
            return JsonResponse(response, status=400)
    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
            # logger.error('User %s', data)
            serializer = InviteesSerializer(invitees, data=data)
            if serializer.is_valid():
                serializer.update(invitees, data)
                return JsonResponse(serializer.data)
            # else:
            #     return JsonResponse(serializer.errors, status=400)

        except BaseException as error:
            # print(error)
            response = {'error': "Error Occurred while updating invitees details"}
            return JsonResponse(response, status=400)

    elif request.method == 'DELETE':
        try:
            invitees.delete()
            return JsonResponse({'deleted': True}, status=200)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while deleting invitees details"}
            return JsonResponse(response, status=400)


today = date.today()


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_multiple_permissions(allowed_permission={'GET': 'get_invitees_detail', 'POST': 'get_invitees_detail'})
def invitees_list(request, org_id, suborg_id):
    today = date.today()
    if request.method == 'GET':
        try:
            invitees = Invitees.objects.filter(org_reference_id=org_id, suborg_reference_id=suborg_id)
            serializer = InviteesSerializer(invitees, many=True)
            return JsonResponse(serializer.data, safe=False)
        except BaseException as error:
            print(error)
            response = {'error': "Error Occurred while getting invitees list"}
            return JsonResponse(response, status=400)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        response = {}
        org_name = org_identifier(org_id)
        suborg_name = suborg_identifier(suborg_id)
        for email in data:
            detail_to_be_sended = {'org_id': org_id, 'suborg_id': suborg_id}
            generated_token = jwt.encode(detail_to_be_sended, 'TokenPassword')
            print(generated_token)
            invitation_email_link = BASE_URL+'?token='+str(generated_token)
            invitee = {
                'invitee_email': email,
                'role_type': data[email],
                'suborg_reference_id': suborg_id,
                'org_reference_id': org_id,
                'sender_id': request.user.id,
                'status type': 'PENDING',
                'email_sent_date': today.strftime("%Y-%m-%d"),
                'invitation_email_link': invitation_email_link
            }
            mail = 'Hii, Welcome to Heartyculture. You are invited to our ' \
                   'suborganisation {} of {} organisation. Click on the link to' \
                   ' proceed {}'.format(org_name, suborg_name, invitation_email_link)

            send_mail('Invite to Heartyculture', mail, 'mytemporary2001@gmail.com', [email], fail_silently=False,)

            serializer = InviteesSerializer(data=invitee)
            response[email] = org_name
            if serializer.is_valid():
                serializer.save()
                response[email] = 'successfully saved'
            else:
                # logger.error('User %s', request.user)
                response[email] = 'invalid credentials'
                # return JsonResponse(serializer.errors, status=400)
        return JsonResponse(response, status=200)


@csrf_exempt
def token_verifier(request):
    token = JSONParser().parse(request)
    decoded = jwt.decode(token['Token'], 'TokenPassword')
    response = {}
    org_id = decoded['org_id']
    suborg_id = decoded['suborg_id']
    # email = ''
    if request.method == 'POST':
        try:
            response['org_name'] = org_id
            response['suborg_name'] = suborg_id
            # response['email'] = email
            return JsonResponse(response, status=200)
        except:
            return JsonResponse(token.errors, status=400)


def org_identifier(org_id):
    try:
        org = Org.objects.get(id=org_id)
        return str(org.name)
    except BaseException as error:
        print(error)
        return "Error Occurred while getting the Org details"


def suborg_identifier(suborg_id):
    try:
        suborg = Suborg.objects.get(id=suborg_id)
        return str(suborg.email)
    except:
        return "Error Occurred while getting the Suborg details"
