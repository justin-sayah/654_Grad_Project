# DDPG Code

DDPG code adapted from [here](https://keras.io/examples/rl/ddpg_pendulum/#introduction).

# Environment Setup

1. Install [Conda](https://docs.conda.io/en/latest/)

2. Create environment:
    ```
    conda env create --file cs654.yml
    ```

3. Start environment:
    ```
    conda activate cs654
    ```

4. Test with:
    ```
    python rl/example_pendulum_train.py
    ```

**After Setup**:

To start environment: run step 3.
To stop environment, run
```
conda deactivate cs654
``` 

## Known Problems

### Linux

Might get following error message on step 4:
```
ImportError: /lib64/libstdc++.so.6: version `GLIBCXX 3.4.21' not found (required by ...
```
Fix:

1. Make sure environment is active:
    ```
    conda activate cs654
    ```
2. Download libgcc:
    ```
    conda install libgcc
    ```
3. Add to path:
    ```
    echo 'export LD_LIBRARY=$LD_LIBRARY_PATH:~/anaconda3/lib' >> ~/.bashrc
    ```