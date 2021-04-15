from rest_framework import serializers
from rest_framework import exceptions
from .models import Poll, Question, Option, Answer
from django.core.exceptions import ObjectDoesNotExist
import datetime


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('__all__')


class QuestionSerializer(serializers.ModelSerializer):
    poll = serializers.SlugRelatedField(slug_field='title', read_only=True, )

    class Meta:
        model = Question
        fields = ('__all__')


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('__all__')

    def create(self, validated_data):
        if validated_data['start_date'] >= validated_data['end_date']:
            raise exceptions.ValidationError('Дата окончания раньше даты начала')
        return Poll.objects.create(**validated_data)


class PollEditSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data.get('title', instance.title)
        if 'end_date' in validated_data:
            try:
                my_end_date = datetime.datetime.strptime(validated_data['end_date'], "%Y-%m-%d").date()
            except ValueError:
                raise exceptions.ValidationError('Неверный формат даты')
            if instance.start_date >= my_end_date:
                raise exceptions.ValidationError('Дата окончания раньше даты начала')
            instance.end_date = validated_data.get('end_date', instance.end_date)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)

        try:
            if 'start_date' in validated_data and datetime.datetime.strptime(validated_data['start_date'],
                                                                             "%Y-%m-%d").date() != instance.start_date:
                raise exceptions.ValidationError('Попытка изменить дату начала опроса')
        except ValueError:
            raise exceptions.ValidationError('Неверный формат даты')

        instance.save()
        return instance


class QuestionCreateSerializer(serializers.ModelSerializer):
    question_poll = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Question
        fields = ('__all__')

    def create(self, validated_data):
        q = Question.objects.create(poll_id=validated_data['poll'], text=validated_data['text'],
                                    type=validated_data['type'])

        if validated_data['type'] == 'OP' or validated_data['type'] == 'MP':
            if 'options' not in validated_data:
                q.delete()
                raise exceptions.ValidationError('Для вопроса с выбором не задан параметр options')
            for opt in validated_data['options']:
                Option.objects.create(question=q, text=opt)

        return q


class QuestionEditSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        if 'poll' in validated_data:
            try:
                int(validated_data['poll'])
                q = Poll.objects.get(id=int(validated_data['poll']))
                instance.poll.id = validated_data.get('poll', instance.poll.id)
            except ValueError:
                raise exceptions.ValidationError('Неверно указан id опроса')
            except ObjectDoesNotExist:
                raise exceptions.ValidationError('Пытаетесь приязать вопрос к несуществующему опросу')

        if 'text' in validated_data:
            if len(validated_data['text']) > 0:
                instance.text = validated_data.get('text', instance.text)
            else:
                raise exceptions.ValidationError('Не пустое поле')

        if 'type' in validated_data:
            if validated_data.get('type') not in ('TX', 'OP', 'MP'):
                raise exceptions.ValidationError('Неверно указан тип вопроса')
            # Перепишем варианты ответа, удалим старые, новые привяжем
            elif validated_data.get('type') in ('OP', 'MP') and 'options' in validated_data:
                instance.type = validated_data.get('type', instance.type)
                for i in instance.options.all():
                    i.delete()
                for opt in validated_data['options']:
                    Option.objects.create(question=instance, text=opt)
            # Удалим варианты, если типо ответа текстовым стал
            elif validated_data.get('type') == 'TX' and instance.type in ('OP', 'MP'):
                instance.type = validated_data.get('type', instance.type)
                for i in instance.options.all():
                    i.delete()
            elif validated_data.get('type') in ('OP', 'MP') and instance.type == 'TX':
                if 'options' not in validated_data:
                    raise exceptions.ValidationError('Укажите опции для вопроса с выбором')
            else:
                instance.type = validated_data.get('type', instance.type)
        elif 'options' in validated_data and instance.type in ('OP', 'MP'):
            for i in instance.options.all():
                i.delete()
            for opt in validated_data['options']:
                Option.objects.create(question=instance, text=opt)

        instance.save()
        return instance


class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ('question',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    options = OptionListSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'options')


class PollDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)

    questions_in_poll = QuestionDetailSerializer(many=True)

    class Meta:
        model = Poll
        exclude = ('id',)


class AnswersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('reply',)


class AnsweredQuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswersListSerializer(many=True)

    class Meta:
        model = Question
        fields = ('text', 'type', 'answers',)


class AnsweredPollDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)

    questions_in_poll = AnsweredQuestionDetailSerializer(many=True)

    class Meta:
        model = Poll
        exclude = ('id',)

# class CreateCompletedPoll(serializers.Serializer):
