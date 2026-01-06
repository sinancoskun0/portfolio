import numpy as np
import pickle
from collections import defaultdict

class QLearningAgent:
    def __init__(
        self,
        actions=3,  # kannst links, rechts, garnix
        learning_rate=0.2, # neue infos nehmen mit 0.1 die alten infos über --- 2 STEPS AHEAD, WAS 0.1 BEFORE
        discount_factor = 0.95, # wie wichtig ist erwartungswert an rewards
        epsilon = 1.0,       # fängt voll random an
        epsilon_min = 0.01, # quasi garnix random mehr bei min, nur noch auf bekannten infos handeln -- WAS 0.001 BEFORE 2 STEPS AHEAD
        epsilon_decay = 0.9996, # wie sehr geht epsilon runter mit der zeit
        lr_decay = 0.9997
    ):
        self.actions = actions
        self.lr = learning_rate
        self.lr_min = 0.01
        self.lr_decay = 0.9995
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

            # hier q-tabelle erstellen, ungesehen states werden mit 0en initialisiert
            # ein key ist: state tupel, die value ist ein array der Q-Werte für jede Aktion
        self.q_table = defaultdict(lambda: np.zeros(self.actions))

    def choose_action(self, state):
        if np.random.random() < self.epsilon:   # wenn die zufällige Zahl zwischen 0-1 kleiner ist als dein Epsilon
            return np.random.randint(self.actions)  # mach random ne Aktion (wird unwahrscheinlicher desto mehr du weißt, desto kleiner dein Epsilon)
        else:
            q_values = self.q_table[state]      # wenn dein Epsilon kleiner war als random-Wert (dh hächstwahrsceinlich hast du schon paar Werte in deiner Q-Tabelle die aktualisiert sind)
                                                # dann nimm den Q-Tabellen-Wert für diesen State mit dem hächsten Erwartungswert-Reward
            max_q = np.max(q_values)            # schau dir deinen max wert an
            best_actions = np.where(q_values == max_q)[0]   # wenn mehrere den max-wert haben
            return np.random.choice(best_actions)   #dann nimm irgendeins von denen, weil alle gleich gut

    def learn(self, state, action, reward, next_state, done):

        current_q = self.q_table[state][action]     # dein aktuelles Q ist der Wert aus der Q-Tab der diesem State & Aktion entspricht

        if done:    # wenn du verlierst
            target = reward # dann kann der Q-Wert für diese state-action-tupel nicht mehr hochgehen, heißt das ist schon der max reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state]) # schau in die tabelle für den erwartungswert der folgt

        # update jetzt deine q-value für diese position
        self.q_table[state][action] += self.lr * (target - current_q)

    def decay_epsilon(self):
        # der soll mit der zeit weniger random werden, heißt epsilon muss runter gehen
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay) # nimm den neuen epsilon wert, oder den min wenn du da schon bist
        self.lr = max(self.lr_min, self.lr * self.lr_decay)

    def save(self, filepath="q_table.pkl"):
        with open(filepath, "wb") as f: # schreibe in q tabelle
            pickle.dump(dict(self.q_table), f)  # speicher instanz des objektes

    def load(self, filepath="q_table.pkl"):
        with open(filepath, "rb") as f:
            loaded = pickle.load(f)
        self.q_table = defaultdict(lambda: np.zeros(self.actions))
        self.q_table.update(loaded)