# api-python-client

## Installation

```bash
pip install forbin
```

## Use

```python
from forbin.client import Client, Submission
from sklearn.ensemble import RandomForestClassifier


client = Client(username='username', password='password')
challenges = client.challenges()
challenge = challenges[0]

clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(challenge.x_train, challenge.y_train)

submission = Submission(client)
submission.confidence = 0.8
submission.stake = 1
submission.y_live = clf.predict(challenge.x_live)
submission.y_test = clf.predict(challenge.x_test)
submission.save()
```