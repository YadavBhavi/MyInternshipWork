from rest_framework import serializers
from .models import Org, Suborg, Invitees, types_of_orgs, types_of_roles, types_of_status


class OrgSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=False)
    corporate_address = serializers.CharField(max_length=100, required=False)
    business_email = serializers.CharField(max_length=100, required=False)
    website = serializers.CharField(max_length=300, required=False)
    contact_no = serializers.CharField(max_length=100, required=False)
    location = serializers.CharField(max_length=300, required=False)
    # logo = serializers.ImageField(read_only=True)
    created_by_id = serializers.IntegerField(required=False)
    foundation_date = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)

    def create(self, validated_data):
        if 'name' not in validated_data:
            raise serializers.ValidationError({'message': 'name is required'})
        return Org.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'coporate_address' in validated_data:
            instance.corporate_address = validated_data['corporate_address']
        if 'business_email' in validated_data:
            instance.business_email = validated_data['business_email']
        if 'website' in validated_data:
            instance.website = validated_data['website']
        if 'contact_no' in validated_data:
            instance.contact_no = validated_data['contact_no']
        if 'location' in validated_data:
            instance.location = validated_data['location']
        if 'created_by_id' in validated_data:
            instance.created_by_id = validated_data['created_by_id']
        if 'foundation_date' in validated_data:
            instance.foundation_date = validated_data['foundation_date']
        instance.save()
        return instance


class SuborgSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    contact_no = serializers.CharField(max_length=100, required=False)
    location = serializers.CharField(max_length=300, required=False)
    type = serializers.ChoiceField(choices=types_of_orgs.choices)
    foundation_date = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)
    created_by_id = serializers.IntegerField(required=False)
    org_reference_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        if 'location' not in validated_data:
            raise Exception(serializers.ValidationError, 'location is required')
        return Suborg.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'address' in validated_data:
            instance.address = validated_data['address']
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'contact_no' in validated_data:
            instance.contact_no = validated_data['contact_no']
        if 'org_reference_id' in validated_data:
            instance.org_reference_id = validated_data['org_reference_id']
        if 'type' in validated_data:
            instance.type = validated_data['type']
        if 'location' in validated_data:
            instance.location = validated_data['location']
        if 'created_by_id' in validated_data:
            instance.created_by_id = validated_data['created_by_id']
        if 'foundation_date' in validated_data:
            instance.foundation_date = validated_data['foundation_date']
        instance.save()
        return instance


class InviteesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    invitee_email = serializers.CharField(max_length=100, required=False)
    invitation_email_link = serializers.CharField(max_length=500, required=False)
    role_type = serializers.ChoiceField(choices=types_of_roles.choices, required=False)
    status_type = serializers.ChoiceField(choices=types_of_status.choices, required=False)
    email_sent_date = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)
    org_reference_id = serializers.IntegerField(required=False)
    sender_id = serializers.IntegerField(required=False)
    suborg_reference_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        if 'invitee_email' not in validated_data:
            raise Exception(serializers.ValidationError, 'invitee_email is required')
        if 'role_type' not in validated_data:
            raise Exception(serializers.ValidationError, 'role_type is required')
        return Invitees.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'invitee_email' in validated_data:
            instance.invitee_email = validated_data['invitee_email']
        if 'invitation_email_link' in validated_data:
            instance.invitation_email_link = validated_data['invitation_email_link']
        if 'role_type' in validated_data:
            instance.role_type = validated_data['role_type']
        if 'status_type' in validated_data:
            instance.status_type = validated_data['status_type']
        if 'org_reference_id' in validated_data:
            instance.org_reference_id = validated_data['org_reference_id']
        if 'sender_id' in validated_data:
            instance.sender_id = validated_data['sender_id']
        if 'suborg_reference_id' in validated_data:
            instance.suborg_reference_id = validated_data['suborg_reference_id']
        if 'email_sent_date' in validated_data:
            instance.email_sent_date = validated_data['email_sent_date']

        instance.save()
        return instance
