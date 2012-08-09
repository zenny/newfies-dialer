#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2012 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib.auth.models import User
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from common.utils import BaseAuthenticatedClient
from survey.models import SurveyApp, SurveyQuestion,\
    SurveyResponse, SurveyCampaignResult
from survey.forms import SurveyForm, SurveyQuestionForm, \
    SurveyResponseForm, SurveyDetailReportForm
from survey.views import survey_list, survey_grid, survey_add, \
    survey_change, survey_del, survey_question_add, survey_question_change,\
    survey_response_add, survey_response_change, survey_report
from datetime import datetime


class SurveyAdminView(BaseAuthenticatedClient):
    """Test Function to check Survey, SurveyQuestion,
       SurveyResponse Admin pages
    """

    def test_admin_surveyapp_view_list(self):
        """Test Function to check admin surveyapp list"""
        response = self.client.get('/admin/survey/surveyapp/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveyapp_view_add(self):
        """Test Function to check admin surveyapp add"""
        response = self.client.get('/admin/survey/surveyapp/add/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveyquestion_view_list(self):
        """Test Function to check admin surveyquestion list"""
        response = self.client.get('/admin/survey/surveyquestion/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveyquestion_view_add(self):
        """Test Function to check admin surveyquestion add"""
        response = self.client.get('/admin/survey/surveyquestion/add/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveyresponse_view_list(self):
        """Test Function to check admin surveyresponse list"""
        response = self.client.get('/admin/survey/surveyresponse/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveyresponse_view_add(self):
        """Test Function to check admin surveyresponse add"""
        response = self.client.get('/admin/survey/surveyresponse/add/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveycampaignresult_view_list(self):
        """Test Function to check admin surveycampaignresult list"""
        response = self.client.get('/admin/survey/surveycampaignresult/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_surveycampaignresult_view_add(self):
        """Test Function to check admin surveycampaignresult add"""
        response = self.client.get('/admin/survey/surveycampaignresult/add/')
        self.failUnlessEqual(response.status_code, 200)


class SurveyCustomerView(BaseAuthenticatedClient):
    """Test Function to check Survey, SurveyQuestion,
       SurveyResponse Customer pages
    """

    fixtures = ['auth_user.json', 'survey.json', 'survey_question.json',
                'survey_response.json']

    def test_survey_view_list(self):
        """Test Function survey view list"""
        response = self.client.get('/survey/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/survey/survey_list.html')

        request = self.factory.get('/survey/')
        request.user = self.user
        request.session = {}
        response = survey_list(request)
        self.assertEqual(response.status_code, 200)

    def test_survey_view_add(self):
        """Test Function survey view add"""
        response = self.client.get('/survey/add/')
        self.assertTrue(response.context['form'], SurveyForm())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/survey/survey_change.html')

        request = self.factory.post('/survey/add/',
                {'name': 'test_survey'}, follow=True)
        request.user = self.user
        request.session = {}
        response = survey_add(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/survey/3/')
        out = Template(
                '{% block content %}'
                    '{% if msg %}'
                        '{{ msg|safe }}'
                    '{% endif %}'
                '{% endblock %}'
            ).render(Context({
                'msg': request.session.get('msg'),
            }))
        self.assertEqual(out, '"test_survey" is added.')

    def test_survey_view_update(self):
        """Test Function survey view get"""
        response = self.client.get('/survey/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/survey/survey_change.html')

        request = self.factory.post('/survey/1/',
                {'name': 'test_survey'}, follow=True)
        request.user = self.user
        request.session = {}
        response = survey_change(request, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/survey/')

        out = Template(
                '{% block content %}'
                    '{% if msg %}'
                        '{{ msg|safe }}'
                    '{% endif %}'
                '{% endblock %}'
            ).render(Context({
                'msg': request.session.get('msg'),
            }))
        self.assertEqual(out, '"test_survey" is updated.')
        self.assertEqual(response.status_code, 302)

        response = survey_del(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_survey_question_view_add(self):
        """Test Function survey question view add"""
        request = self.factory.post('/survey_question/add/?surveyapp_id=1',
                {'question': 'test_question', 'type': 1})
        request.user = self.user
        request.session = {}
        response = survey_question_add(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'frontend/survey/survey_question_change.html')

    def test_survey_question_view_update(self):
        """Test Function survey question view update"""
        request = self.factory.post('/survey_question/1/',
                {'question': 'test_question', 'type': 1})
        request.user = self.user
        request.session = {}
        response = survey_question_change(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'frontend/survey/survey_question_change.html')

    def test_survey_question_response_view_add(self):
        """Test Function survey response view add"""
        request = self.factory.post('/survey_response/add/?surveyquestion_id=1',
                {'key': '1', 'keyvalue': 'apple'})
        request.user = self.user
        request.session = {}
        response = survey_response_add(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'frontend/survey/survey_response_change.html')

    def test_survey_question_response_view_update(self):
        """Test Function survey response view update"""
        request = self.factory.post('/survey_response/1/',
                {'key': '1', 'keyvalue': 'apple'})
        request.user = self.user
        request.session = {}
        response = survey_response_change(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'frontend/survey/survey_response_change.html')

    def test_survey_view_report(self):
        """Test Function survey view report"""
        request = self.factory.post('/survey_report/',
                                    {'campaign': 1,
                                     'from_date': datetime.now(),
                                     'to_date': datetime.now()})
        request.user = self.user
        request.session = {}
        response = survey_report(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/survey/survey_report.html')

        response = self.client.post('/survey_report/',
                                    {'campaign': 1,
                                     'from_date': datetime.now(),
                                     'to_date': datetime.now()})
        self.assertTrue(response.context['form'],
                        SurveyDetailReportForm(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/survey/survey_report.html')

        # Test template tags
        out = Template(
                '{% load dialer_cdr_extras common_tags %}'
                '{% block content %}'
                    '{{ duration|conv_min }}'
                    '{{ question_response|que_res_string|safe }}'
                    '{{ duration|cal_width:max_duration }}'
                '{% endblock %}'
            ).render(Context({
                'duration': 60,
                'question_response': 'qst_1*|*ans_1',
                'max_duration': 100
            }))
        self.assertEqual(out,
            '01:00'
            '<table class="table table-striped table-bordered table-condensed">'
            '<tr><td>qst_1</td><td class="survey_result_key">ans_1</td></tr>'
            '</table>'
            '120.0')


class SurveyModel(TestCase):
    """Test Survey, SurveyQuestion, SurveyResponse Model"""

    fixtures = ['gateway.json', 'auth_user.json', 'contenttype.json',
                'phonebook.json', 'contact.json',
                'campaign.json', 'campaign_subscriber.json',
                'callrequest.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')

        # SurveyApp model
        self.survey = SurveyApp(
            name='test_survey',
            user=self.user,
        )
        self.survey.save()

        # SurveyQuestion model
        self.survey_question = SurveyQuestion(
            question='test_question',
            user=self.user,
            surveyapp=self.survey,
        )
        self.survey_question.save()

        # SurveyResponse model
        self.survey_response = SurveyResponse(
            key='5',
            keyvalue='egg',
            surveyquestion=self.survey_question,
        )
        self.survey_response.save()

        # SurveyCampaignResult model
        self.survey_result = SurveyCampaignResult(
            surveyapp=self.survey,
            question='test_question',
            response='5',
            callrequest_id=None,
        )
        self.survey_result.save()

    def test_survey_forms(self):
        self.assertEqual(self.survey.name, "test_survey")
        self.assertEqual(self.survey_question.question, "test_question")
        self.assertEqual(self.survey_response.key, "5")
        self.assertEqual(self.survey_result.surveyapp, self.survey)

        form = SurveyQuestionForm(self.user)
        obj = form.save(commit=False)
        obj.question="test question"
        obj.user = self.user
        obj.surveyapp = self.survey
        obj.save()

        form = SurveyResponseForm(self.user, self.survey.pk)
        obj = form.save(commit=False)
        obj.key="1"
        obj.keyvalue="apple"
        obj.surveyquestion = self.survey_question
        obj.save()

    def teardown(self):
        self.survey.delete()
        self.survey_question.delete()
        self.survey_response.delete()
        self.survey_result.delete()
