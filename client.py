import pandas as pd
import requests
from typing import Union


class Challenge:
    def __init__(self, data=None, dataset_id=None, submission_start_date=None,
                 submission_end_date=None, x=None, y=None) -> None:
        self.id = data.get('id')
        self.dataset_id = data.get('dataset_id', dataset_id)
        self.submission_start_date = data.get('submission_start_date', submission_start_date)
        self.submission_end_date = data.get('submission_end_date', submission_end_date)
        self.x = pd.DataFrame(data=data.get('x', x))
        self.y = pd.DataFrame(data=data.get('y', y))



class Dataset:
    def __init__(self, data=None, date=None, x=None, y=None) -> None:
        self.id = data.get('id')
        self.date = data.get('date', date)
        self.x = pd.DataFrame(data=data.get('x', x))
        self.y = pd.DataFrame(data=data.get('y', y))


class Submission:
    def __init__(self, data=None, challenge_id=None, submission_date=None,
                 user_id=None, y=None) -> None:
        self.id = data.get('id')
        self.challenge_id = data.get('challenge_id', challenge_id)
        self.submission_date = data.get('submission_date', submission_date)
        self.user_id = pd.DataFrame(data=data.get('user_id', user_id))
        self.y = pd.DataFrame(data=data.get('y', y))


class Client:

    def __init__(self, username, password, api_endpoint='http://localhost:8000/api'):
        self.api_endpoint = api_endpoint
        self.token = None
        response = requests.post(
            f'{api_endpoint}/token', data={'username': username, 'password': password})
        if response.status_code != 200:
            return print(response.json())
        self.token = response.json()['token']
    
    def _delete(self, route, data):
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
            f'{self.api_endpoint}/{route}/', data=data, headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()
    
    def _post(self, route, data):
        response = requests.post(
            f'{self.api_endpoint}/{route}/', data=data, headers={'Authorization': f'Token {self.token}'})
        if response.status_code != 200:
            return print(response.json())
        return response.json()

    @property
    def challenge(self) -> Union[Challenge, list[Challenge]]:
        data = self._get(route='challenges')
        if len(data) == 1:
            return Challenge(data[-1])
        return [Challenge(d) for d in data]
    
    @challenge.deleter
    def challenge(self, value: Challenge):
        return self._delete(route=f'challenges/{value.id}')

    @challenge.setter
    def challenge(self, value: Challenge):
        data = {
            'dataset_id': value.dataset_id,
            'submission_start_date': value.submission_start_date,
            'submission_end_date': value.submission_end_date,
            'x': value.x.to_dict(orient='records'),
            'y': value.y.to_dict(orient='records')
        }
        if value.id:
            return self._patch(route=f'challenges/{value.id}', data=data)
        return self._post(route='challenges', data=data)

    @property
    def dataset(self) -> Union[Dataset, list[Dataset]]:
        data = self._get(route='datasets')
        if len(data) == 1:
            return Dataset(data[-1])
        return [Dataset(d) for d in data]
    
    @dataset.setter
    def dataset(self, value: Dataset):
        data = {
            'date': value.date.isoformat(),
            'x': value.x.to_dict(orient='records'),
            'y': value.y.to_dict(orient='records')
        }
        return self._post(route='datasets', data=data)

    @property
    def submission(self) -> Union[Submission, list[Submission]]:
        data = self._get(route='submissions')
        if len(data) == 1:
            return Submission(data[-1])
        return [Submission(d) for d in data]

    @submission.setter
    def submission(self, value: Submission):
        data = {
            'y': value.y.to_dict(orient='records')
        }
        return self._post(route='submissions', data=data)


if __name__ == '__main__':
    client = Client(username='test', password='abc1234!')
    print(client.dataset)
    print(client.challenge)
    print(client.submission)
