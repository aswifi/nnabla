# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import nnabla.functions as F
from .utils import no_grad


def huber_loss_backward(inputs, delta=1.0):
    """
    Args:
      inputs (list of nn.Variable): Incomming grads/inputs to/of the forward function.
      kwargs (dict of arguments): Dictionary of the corresponding function arguments.

    Return:
      list of Variable: Return the gradients wrt inputs of the corresponding function.
    """
    dy = inputs[0]
    x0 = inputs[1]
    x1 = inputs[2]
    d = x0 - x1
    m0 = F.less_scalar(F.abs(d), delta)
    m1 = 1 - m0
    mg = F.greater(x0, x1)
    ml = 1 - mg
    m0 = no_grad(m0)
    m1 = no_grad(m1)
    mg = no_grad(mg)
    ml = no_grad(ml)
    t0 = 2 * d * m0
    t1 = 2 * delta * m1 * mg
    t2 = -2 * delta * m1 * ml
    dx0 = dy * (t0 + t1 + t2)
    dx1 = -dx0
    return dx0, dx1
