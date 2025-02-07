from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'password', 'is_superuser']

    def create(self, validated_data):
        """ 사용자 생성 시 비밀번호를 해싱해서 저장 """
        user = User(
            nickname=validated_data['nickname'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # ✅ 비밀번호 해싱
        user.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'password', 'profile_image']
        READ_ONLY_FIELDS = ['id', 'email']

    def update(self, instance, validated_data):
        # 닉네임 업데이트
        instance.nickname = validated_data.get('nickname', instance.nickname)

        # 비밀번호 업데이트
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), **attrs)
            if not user:
                raise serializers.ValidationError(
                    detail='Unable to log in with provided credentials.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                detail='Must be Required "email" and "password".', code='authorization'
            )

        attrs['user'] = user
        return attrs