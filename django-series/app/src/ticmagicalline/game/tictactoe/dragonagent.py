import numpy as np
import tensorflow as tf

class DragonAgent:
    def __init__(self, alpha=0.5, discount=0.95, exploration_rate=1.0):
        self.alpha = alpha
        self.discount = discount
        self.exploration_rate = exploration_rate
        self.state = None
        self.action = None

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, input_shape=(9,), activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(9)
        ])

        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=alpha), loss='mse')

    def start(self, state):
        self.state = np.array(state)
        self.action = self.get_action(state)
        return self.action

    def get_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            action = np.random.choice(9)
        else:
            q_values = self.model.predict(np.array([state]))
            action = np.argmax(q_values[0])
        return action

    def learn(self, state, action, reward, next_state):
        q_update = reward
        if next_state is not None:
            q_values_next = self.model.predict(np.array([next_state]))
            q_update += self.discount * np.max(q_values_next[0])

        q_values = self.model.predict(np.array([state]))
        q_values[0][action] = q_update

        self.model.fit(np.array([state]), q_values, verbose=0)

        self.exploration_rate *= 0.99

    def step(self, state, reward):
        action = self.get_action(state)
        self.learn(self.state, self.action, reward, state)
        self.state = np.array(state)
        self.action = action
        return action
