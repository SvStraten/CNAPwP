# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:05:12 2024

@author: Tamara Verbeek
"""

def get_args_parser(subparsers):
    subparsers.add_argument('--batch_size', default=15, type=int, help='Batch size')
    subparsers.add_argument('--epochs', default=5, type=int)
    subparsers.add_argument('--init_epochs', default=40, type=int)
    subparsers.add_argument('--attributes', default=None, type=str)
    subparsers.add_argument('--prefix_length', default=30, type=int)
    subparsers.add_argument('--window_size', default=350, type=int)
    subparsers.add_argument('--init_size', default=500, type=int)
    subparsers.add_argument('--init_batch_size', default=50, type=int, help='Batch size for initialization')
    subparsers.add_argument('--buffer_size', default = 100, type = int)
    subparsers.add_argument('--boundary', default = 0.5, type = int)
    subparsers.add_argument('--prefix', default = True)

    # Model parameters
    subparsers.add_argument('--model', default='IOR', type=str, metavar='MODEL', help='Name of model to train')
    subparsers.add_argument('--input_size', default=int, type=int, help='input size')
    subparsers.add_argument('--hidden_size', default=20, help='hidden size')
    subparsers.add_argument('--attn_drop', type=float, default=0.0, metavar='PCT', help='Dropout rate (default: 0.)')
    subparsers.add_argument('--proj_drop', type=float, default=0.0, metavar='PCT', help='Dropout rate (default: 0.)')
    subparsers.add_argument('--output_size', default=int, help='output size')
    subparsers.add_argument('--num_heads', default=1, help='Number of output heads')
    
    # Optimizer parameters
    subparsers.add_argument('--opt', default='nadam', type=str, metavar='OPTIMIZER', help='Optimizer (default: "adam"')
    subparsers.add_argument('--opt_eps', default=1e-8, type=float, metavar='EPSILON', help='Optimizer Epsilon (default: 1e-8)')
    subparsers.add_argument('--opt_betas', default=(0.9, 0.999), type=float, nargs='+', metavar='BETA', help='Optimizer Betas (default: (0.9, 0.999), use opt default)')
    subparsers.add_argument('--weight_decay', type=float, default=0.0, help='weight decay (default: 0.0)')

    # Learning rate schedule parameters
    subparsers.add_argument('--lr', type=float, default=0.002, metavar='LR', help='learning rate (default: 0.03)')

    # Pruning Tree parameters
    subparsers.add_argument('--pruningSteps', default=1000, type=int)
    subparsers.add_argument('--noiseFilter', default=1, type=int)
    subparsers.add_argument('--lambdaDecay', type=float, default=0.25)
    
    # Data parameters
    subparsers.add_argument('--data-path', default='local_datasets/', type=str, help='dataset path')
    subparsers.add_argument('--dataset', default='IOR_tasks.csv', type=str, help='dataset name')
    subparsers.add_argument('--output_dir', default='./output', help='path where to save, empty for no saving')
    subparsers.add_argument('--device', default='cpu', help='device to use for training / testing')
    subparsers.add_argument('--seed', default=42, type=int)
    subparsers.add_argument('--output_file', default = "output", type =str, help ='output filename')
    subparsers.add_argument('--nrOfEvents', type=int, help='Number of events')
    subparsers.set_defaults(pin_mem=True)

    # G-Prompt parameters
    subparsers.add_argument('--use_g_prompt', default=True, type=bool, help='if using G-Prompt')
    subparsers.add_argument('--g_prompt_length', default=5, type=int, help='length of G-Prompt')
    subparsers.add_argument('--g_prompt_layer_idx', default=[0, 1], type=int, nargs = "+", help='the layer index of the G-Prompt')
    
    # E-Prompt parameters
    subparsers.add_argument('--use_e_prompt', default=True, type=bool, help='if using the E-Prompt')
    subparsers.add_argument('--e_prompt_layer_idx', default=[2, 3, 4], type=int, nargs = "+", help='the layer index of the E-Prompt')
    subparsers.add_argument('--prompt_prefix_size', default=5, type=int,)
    subparsers.add_argument('---encodedFirstEvents', default = None)

    # Use prompt pool in L2P to implement E-Prompt
    subparsers.add_argument('--e_prompt_length', default=10, type=int,)
    subparsers.add_argument('--length', default=10,type=int, )
    subparsers.add_argument('--initializer', default='uniform', type=str,)

    # Misc parameters
    subparsers.add_argument('--print_freq', type=int, default=10, help = 'The frequency of printing')