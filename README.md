# NYC Taxi Pipeline

## Run

```python
from pipeline import build_pipeline
model = build_pipeline()
model.fit(X_train, y_train)
```

The pipeline automatically handles missing values, categorical encoding, unseen categories, and robust scaling before training a Linear Regression model.
