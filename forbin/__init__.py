from datetime import datetime
from typing import Union

import pandas as pd
import pytz
import requests


class Object:
    def __init__(self, client=None, data=None) -> None:
        self._client = client
        self.id = data.get('id')
        created_at = data.get('created_at')
        self.created_at = \
            datetime.fromisoformat(created_at[:-1]).replace(tzinfo=pytz.UTC) \
                if created_at else created_at
    
    def __str__(self) -> str:
        return {
            'id': self.id,
            'created_at': self.created_at,
        }.__str__()
    
    def delete(self) -> None:
        """
        Delete object.
        Parameters:
        -----------
        Returns:
        --------
        """
        self._client._delete(route=f'{self._subroute}/{self.id}')
    
    def save(self):
        """
        Save object.
        Parameters:
        -----------
        Returns:
        --------
        """
        if self.id:
            return self._client._patch(route=f'{self._subroute}/{self.id}', data=self.__dict__())
        return self._client._post(route=f'{self._subroute}', data=self.__dict__())
        


class Challenge(Object):
    
    _subroute = 'challenges'

    def __init__(self, client=None, data={}) -> None:
        super().__init__(client, data)
        self.finished = data.get('finished')
        self.prize = data.get('prize')
        submission_start = data.get('submission_start')
        self.submission_start = \
            datetime.fromisoformat(submission_start[:-1]).replace(tzinfo=pytz.UTC) \
                if submission_start else submission_start
        submission_end = data.get('submission_end')
        self.submission_end = \
            datetime.fromisoformat(submission_end[:-1]).replace(tzinfo=pytz.UTC) \
                if submission_end else submission_end
        self.x_live = pd.DataFrame(data=data.get('x_live'))
        self.x_test = pd.DataFrame(data=data.get('x_live'))
        self.x_train = pd.DataFrame(data=data.get('x_live'))
        self.y_train = pd.DataFrame(data=data.get('x_live'))
    
    def __dict__(self) -> dict:
        data = {
            'id': self.id,
            'finished': self.finished,
            'prize': self.prize,
            'submission_start': self.submission_start.isoformat(),
            'submission_end': self.submission_end.isoformat(),
            'x_live': self.x_live.to_dict(orient='records'),
            'x_test': self.x_test.to_dict(orient='records'),
            'x_train': self.x_train.to_dict(orient='records'),
            'y_train': self.y_train.to_dict(orient='records'),
        }
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data
    
    

class GroundTruth(Object):

    _subroute = 'groundtruths'

    def __init__(self, client=None, data={}) -> None:
        super().__init__(client, data)
        self.challenge_id = data.get('challenge_id')
        self.y_live = pd.DataFrame(data=data.get('y_live'))
        self.y_test = pd.DataFrame(data=data.get('y_test'))
    
    def __dict__(self) -> dict:
        data = {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'y_live': self.y_live.to_dict(orient='records'),
            'y_test': self.y_test.to_dict(orient='records'),
        }
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data

class Submission(Object):
    
    _subroute = 'submissions'

    def __init__(self, client=None, data={}) -> None:
        super().__init__(client, data)
        self.challenge_id = data.get('challenge_id')
        self.confidence = data.get('confidence')
        self.consistency = data.get('consistency')
        self.logloss = data.get('logloss')
        self.originality = data.get('originality')
        self.reward = data.get('reward')
        self.stake = data.get('stake')
        self.user_id = data.get('user_id')
        self.y_live = pd.DataFrame(data=data.get('y_live'))
        self.y_test = pd.DataFrame(data=data.get('y_test'))
    
    def __dict__(self) -> dict:
        data = {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'confidence': self.confidence,
            'consistency': self.consistency,
            'logloss': self.logloss,
            'originality': self.originality,
            'reward': self.reward,
            'stake': self.stake,
            'user_id': self.user_id,
            'y_live': self.y_live.to_dict(orient='records'),
            'y_test': self.y_test.to_dict(orient='records'),
        }
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data

class Transaction(Object):
    
    _subroute = 'transactions'

    def __init__(self, client=None, data={}) -> None:
        super().__init__(client, data)
        self.challenge_id = data.get('challenge_id')
        self.amount = data.get('amount')
        self.category = data.get('category')
        self.user_id = data.get('user_id')
    
    def __dict__(self) -> dict:
        data =  {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'amount': self.amount,
            'category': self.category,
            'user_id': self.user_id,
        }
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data


class Client:

    def __init__(self, username, password, api_endpoint='https://app.forbin-capital.com/api'):
        self.api_endpoint = api_endpoint
        self.token = None
        response = requests.post(
            f'{api_endpoint}/token', data={'username': username, 'password': password})
        if response.status_code != 200:
            return print(response.json())
        self.token = response.json()['token']
    
    def _delete(self, route):
        response = requests.delete(
            f'{self.api_endpoint}/{route}/', headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()

    def _get(self, route):
        response = requests.get(
            f'{self.api_endpoint}/{route}/', headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()
    
    def _patch(self, route, data):
        response = requests.patch(
            f'{self.api_endpoint}/{route}/', json=data, headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()
    
    def _post(self, route, data):
        response = requests.post(
            f'{self.api_endpoint}/{route}/', json=data, headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()

    def challenges(self, id=None) -> Union[Challenge, list[Challenge]]:
        """
        Get challenges.
        Parameters:
        -----------
        id : string
            Challenge ID.
        Returns:
        --------
        Either a list of Challenge objects or one Challenge object.
        """
        data = self._get(route='challenges')
        return [Challenge(client=self, data=d) for d in data]
    
    def ground_truths(self, id=None) -> Union[GroundTruth, list[GroundTruth]]:
        """
        Get ground truths.
        Parameters:
        -----------
        id : string
            GroundTruth ID.
        Returns:
        --------
        Either a list of GroundTruth objects or one GroundTruth object.
        """
        data = self._get(route='groundtruths')
        return [GroundTruth(client=self, data=d) for d in data]
    
    def submissions(self, id=None) -> Union[Submission, list[Submission]]:
        """
        Get submissions.
        Parameters:
        -----------
        id : string
            Submission ID.
        Returns:
        --------
        Either a list of Submission objects or one Submission object.
        """
        data = self._get(route='submissions')
        return [Submission(client=self, data=d) for d in data]
    
    def transactions(self, id=None) -> Union[Transaction, list[Transaction]]:
        """
        Get transactions.
        Parameters:
        -----------
        id : string
            Transaction ID.
        Returns:
        --------
        Either a list of Transaction objects or one Transaction object.
        """
        data = self._get(route='transactions')
        return [Transaction(client=self, data=d) for d in data]
    
    
    


