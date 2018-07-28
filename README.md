# Using Deep Q Networks to learn Space Shooter

#### Dhruva Bansal, Hemang Rajvanshy

# 1. Abstract

We use a Deep Q Network introduced by the pioneering paper by DeepMind: [Playing Atari with Deep Reinforcement Learning](https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf) to teach the computer a variation of the Space Shooter game. The aim is to learn the game without any guided input by learning directly from the game screen, given the same inputs a human would receive to learn the game. By doing so, we aim to test the generalizability of the algorithm to more complicated problems and to test its limitations. We found that the network showed improvements with training and performed better than random, but failed to reach human level in the limited amount of training we could perform.  

# 2. Background

Reinforcement learning combines aspects of both supervised and unsupervised learning to create sparse, time-delayed labels called rewards. Based on these rewards, the agent has to learn how to interact and behave in the environment. 

We specifically used a method called Q-learning which uses a Q(s,a) to approximate the maximum discounted future reward when action a in state s is performed. 

Given a run of the Markov decision process, reward R can be calculated as:

Given this, total reward from a point t can be calculated as:

Due to a stochastic environment, there is a high possibility the rewards diverge the more into future we go. Hence, using a discount factor Y between 0 and 1, we reduce the weightage of the reward the more into future it is. Hence the new discounted future reward is:

This can also be expressed as:

Using the above expression for Q(s,a) and the Bellman equation:

We iteratively approximate the maximum future reward for this state.

Q-learning algorithm:

*Initialize Q[num_states, num_actions] arbitrarily*

*Observe initial state s*

*Repeat*

*	Select and carry out an action a *

*	Observe reward r and new state s’*

*Until terminated*

# 3. Methods

### Game Interface

We removed powerups from the game in order to decrease the number of variable parameters and to simplify training. The score and health GUI texts, along with the background  were also removed from the game screen in order to make the network converge faster. The program received the scores directly from the game and interacted with it in the form of a binary array of size four, representing the possible actions in the game. 

### Network Architecture

As in ([1.](#heading=h.nda55hrhql2o)), we perform the following preprocessing on the game screens:

1. Convert image to grayscale.

2. Resize image to 80x80.

3. Stack last 4 frames to produce an 80x80x4 input array for network.

The architecture of the network is shown in the figure below. The first layer convolves the input image with an 8x8x4x32 kernel at a stride size of 4. The output is then put through a 2x2 max pooling layer. The second layer convolves with a 4x4x32x64 kernel at a stride of 2. We then max pool again. The third layer convolves with a 3x3x64x64 kernel at a stride of 1. We then max pool one more time. The last hidden layer consists of 256 fully connected ReLU nodes.

![image alt text](https://i.imgur.com/XwHUHwa.png "Network Architecture")

The final output is an array whose length is the same as the number of possible actions that can be performed in the game. The values at this output layer represent the Q function given the input state for each valid action. At each time step, the network performs whichever action corresponds to the highest Q value using an epsilon greedy strategy.

### Training

We initialized the network weights randomly using a normal distribution with a standard deviation of 0.01 and set the replay memory with a max size of 50,000 experiences. 

We initially let the network observe the game for 10,000 time steps by choosing random actions. This allows us to populate the replay memory. 

After that, we linearly anneal ϵ from INITIAL_EPSILON to FINAL_EPSILON over the course of the EXPLORATION phase. During this time, at each time step, the network samples mini-batches of size 32 from the replay memory to train on, and performs a gradient step on the loss function described above using the Adam optimization algorithm with a learning rate of 0.000001. After annealing finishes, the network continues to train indefinitely, with ϵ fixed at FINAL_EPSILON.

We tried various values for the parameters INITIAL_EPSILON, FINAL_EPSILON, and the duration of the EXPLORATION phase in order to find optimal performance. 

Google Colaboratory as well as local hardware was used for training. 

# 4. Results

We found that for this Space Shooter game, results were achieved after about 500,000 iterations which corresponds to about 5 hours of game time. The network showed improvements with training and performed better than random, but failed to reach human level in the limited amount of training we could perform.  

Our tested values for gamma and learning rate are 0.95 and 1e-6 respectively. We would like to experiment further to find optimal values of rewards, gamma, epsilon, and learning rate in the future. We would also like to try optimising the algorithm by adding a Huber Loss function to handle rewards and training using target networks. However, due to limited access to GPUs, we were unable to complete a detailed analysis.  

<table>
  <caption align="bottom"> <b> Average scores (100 games) DQN trained to 500,000 iterations </b></caption>
  <tr>
    <td>Random</td>
    <td>DQN</td>
    <td>Bot</td>
  </tr>
  <tr>
    <td>132.1</td>
    <td>258.4</td>
    <td>459.0</td>
  </tr>
</table>


We experimented with various reward schemes and the most optimal results were found when we adopted a [+1, -0.9] for scoring and taking a hit respectively. The trained net still displayed a tendency to stick to the corners of the game screen where the density of enemy shooters is low and the chances of getting hit is minimized. We would like to experiment further and see what happens when the negative reward for getting hit is minimized further or eliminated completely. 

# References

1. Akshay Srivatsan, Ivan Kuznetsov, Willis Wang. Using Deep Q Networks to Learn Video Game Strategies.
[https://github.com/asrivat1/DeepLearningVideoGames](https://github.com/asrivat1/DeepLearningVideoGames)

2. Tambet Matiisen. Demystifying Deep Reinforcement Learning. <br>
[https://ai.intel.com/demystifying-deep-reinforcement-learning/](https://ai.intel.com/demystifying-deep-reinforcement-learning/)

The game used in this project is a modified version of Space Shooter (based on the retro space shooter game) by Tyler Gray
[https://www.pygame.org/project-Space+Shooter-1292-.html](https://www.pygame.org/project-Space+Shooter-1292-.html)

