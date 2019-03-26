#! /usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, os

sys.path.append("./")

import logging
import argparse

from inference.estimator import ParameterizedRatioEstimator

logging.basicConfig(format="%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s", datefmt="%H:%M", level=logging.DEBUG)


def train(
    method, alpha, data_dir, sample_name, model_filename, log_input=False, batch_size=256, n_epochs=5, optimizer="adam", initial_lr=0.001, final_lr=0.0001, limit_samplesize=None
):
    estimator = ParameterizedRatioEstimator(resolution=64, n_parameters=2, log_input=log_input, rescale_inputs=True)
    estimator.train(
        method,
        x="{}/samples/x_{}.npy".format(data_dir, sample_name),
        y="{}/samples/y_{}.npy".format(data_dir, sample_name),
        theta="{}/samples/theta_{}.npy".format(data_dir, sample_name),
        r_xz="{}/samples/r_xz_{}.npy".format(data_dir, sample_name),
        t_xz="{}/samples/t_xz_{}.npy".format(data_dir, sample_name),
        alpha=alpha,
        optimizer=optimizer,
        n_epochs=n_epochs,
        batch_size=batch_size,
        initial_lr=initial_lr,
        final_lr=final_lr,
        nesterov_momentum=None,
        validation_split=0.25,
        early_stopping=True,
        limit_samplesize=limit_samplesize,
        verbose="all",
    )
    estimator.save("{}/models/{}".format(data_dir, model_filename))


def parse_args():
    parser = argparse.ArgumentParser(description="Strong lensing experiments: simulation")

    # Main options
    parser.add_argument("method", help='Inference method: "carl", "rolr", "alice", "cascal", "rascal", "alices".')
    parser.add_argument("--sample", type=str, default="train", help='Sample name, like "train".')
    parser.add_argument("--name", type=str, default=None, help="Model name. Defaults to the name of the method.")
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Directory. Training data will be loaded from the data/samples subfolder, the model saved in the data/models subfolder.",
    )

    # Training options
    parser.add_argument(
        "--alpha",
        type=float,
        default=1.0,
        help="alpha parameter weighting the score MSE in the loss function of the SCANDAL, RASCAL, and" "and ALICES inference methods. Default: 1.",
    )
    parser.add_argument("--log", action="store_true", help="Whether the log of the input is taken.")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs. Default: 5.")
    parser.add_argument("--batch_size", type=int, default=256, help="Batch size. Default: 256.")
    parser.add_argument("--optimizer", default="adam", help='Optimizer. "amsgrad", "adam", and "sgd" are supported. Default: "adam".')
    parser.add_argument("--initial_lr", type=float, default=0.001, help="Initial learning rate. Default: 0.001.")
    parser.add_argument("--final_lr", type=float, default=0.00001, help="Final learning rate. Default: 0.00001.")
    parser.add_argument("--validation_split", type=float, default=0.3, help="Validation split. Default: 0.3.")

    return parser.parse_args()


if __name__ == "__main__":
    logging.info("Hi!")

    args = parse_args()

    train(
        method=args.method,
        alpha=args.alpha,
        data_dir="{}/data/".format(args.dir),
        sample_name=args.sample,
        model_filename=args.name,
        log_input=args.log,
        batch_size=args.batch_size,
        n_epochs=args.epochs,
        optimizer=args.optimizer,
        initial_lr=args.initial_lr,
        final_lr=args.final_lr,
    )

    logging.info("All done! Have a nice day!")
