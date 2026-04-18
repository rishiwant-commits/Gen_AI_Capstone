import numpy as np
import pandas as pd

def get_feature_contributions(model, input_df, scaler, columns):
    """
    Returns feature-wise contribution to prediction
    """

    # Step 1: Scale input (same as model)
    scaled_input = scaler.transform(input_df)

    # Step 2: Get model coefficients
    coefs = model.coef_

    # Step 3: Multiply feature values with coefficients
    contributions = scaled_input[0] * coefs

    # Step 4: Create dataframe
    contribution_df = pd.DataFrame({
        "Feature": columns,
        "Contribution": contributions
    })

    # Step 5: Sort by impact
    contribution_df = contribution_df.sort_values(
        by="Contribution",
        key=abs,
        ascending=False
    )

    return contribution_df