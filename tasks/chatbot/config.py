"""Various configuration options for the chatbot task.

This file is intended to be modified. You can go in and change any
of the variables to run different experiments.
"""

from __future__ import annotations

from typing import Any

import transformers

from zeno_build.evaluation.text_features.length import input_length, output_length
from zeno_build.evaluation.text_metrics.critique import (  # avg_toxicity,; toxicity,
    avg_bert_score,
    avg_chrf,
    avg_length_ratio,
    bert_score,
    chrf,
    length_ratio,
)
from zeno_build.experiments import search_space
from zeno_build.models.lm_config import LMConfig
from zeno_build.prompts.chat_prompt import ChatMessages, ChatTurn

# Define the space of hyperparameters to search over.
space = {
    "prompt_preset": search_space.Categorical(
        ["standard", "friendly", "polite", "cynical"]
    ),
    "model_preset": search_space.Categorical(
        [
            "gpt-3.5-turbo",
            "cohere-command-xlarge" "gpt2",
            "gpt2-xl",
            "llama-7b",
            "alpaca-7b",
            "vicuna-7b",
        ]
    ),
    "temperature": search_space.Discrete([0.2, 0.3, 0.4]),
}

# Any constants that are not searched over
constants: dict[str, Any] = {
    "test_dataset": "daily_dialog",
    "test_split": "validation",
    "test_examples": 1000,
    "max_tokens": 100,
    "top_p": 1.0,
}

# The number of trials to run
num_trials = 1000

# The details of each model
model_configs = {
    "text-davinci-003": LMConfig(provider="openai", model="text-davinci-003"),
    "gpt-3.5-turbo": LMConfig(provider="openai_chat", model="gpt-3.5-turbo"),
    "cohere-command-xlarge": LMConfig(
        provider="cohere", model="command-xlarge-nightly"
    ),
    "gpt2": LMConfig(
        provider="huggingface",
        model="gpt2",
        model_cls=transformers.GPT2LMHeadModel,
    ),
    "gpt2-xl": LMConfig(
        provider="huggingface",
        model="gpt2-xl",
        model_cls=transformers.GPT2LMHeadModel,
    ),
    "llama-7b": LMConfig(
        provider="huggingface",
        model="decapoda-research/llama-7b-hf",
        tokenizer_cls=transformers.LlamaTokenizer,
    ),
    "llama-13b": LMConfig(
        provider="huggingface",
        model="decapoda-research/llama-13b-hf",
        tokenizer_cls=transformers.LlamaTokenizer,
    ),
    "alpaca-7b": LMConfig(
        provider="huggingface",
        model="chavinlo/alpaca-native",
    ),
    "alpaca-13b": LMConfig(
        provider="huggingface",
        model="chavinlo/alpaca-13b",
    ),
    "vicuna-7b": LMConfig(
        provider="huggingface",
        model="eachadea/vicuna-7b-1.1",
        user_name="HUMAN",
        system_name="ASSISTANT",
    ),
    "vicuna-13b": LMConfig(
        provider="huggingface",
        model="eachadea/vicuna-7b-1.1",
        user_name="HUMAN",
        system_name="ASSISTANT",
    ),
}

# The details of the prompts
prompt_messages: dict[str, ChatMessages] = {
    "standard": ChatMessages(
        messages=[
            ChatTurn(
                role="system",
                content="You are a chatbot tasked with making small-talk with "
                "people.",
            ),
            ChatTurn(role="system", content="{{context}}"),
            ChatTurn(role="user", content="{{source}}"),
        ]
    ),
    "friendly": ChatMessages(
        messages=[
            ChatTurn(
                role="system",
                content="You are a kind and friendly chatbot tasked with making "
                "small-talk with people in a way that makes them feel "
                "pleasant.",
            ),
            ChatTurn(role="system", content="{{context}}"),
            ChatTurn(role="user", content="{{source}}"),
        ]
    ),
    "polite": ChatMessages(
        messages=[
            ChatTurn(
                role="system",
                content="You are an exceedingly polite chatbot that speaks very "
                "formally and tries to not make any missteps in your "
                "responses.",
            ),
            ChatTurn(role="system", content="{{context}}"),
            ChatTurn(role="user", content="{{source}}"),
        ]
    ),
    "cynical": ChatMessages(
        messages=[
            ChatTurn(
                role="system",
                content="You are a cynical chatbot that has a very dark view of the "
                "world and in general likes to point out any possible "
                "problems.",
            ),
            ChatTurn(role="system", content="{{context}}"),
            ChatTurn(role="user", content="{{source}}"),
        ]
    ),
}

# The functions to use to calculate scores for the hyperparameter sweep
sweep_distill_functions = [chrf]
sweep_metric_function = avg_chrf

# The functions used for Zeno visualization
zeno_distill_and_metric_functions = [
    output_length,
    input_length,
    avg_chrf,
    chrf,
    avg_length_ratio,
    length_ratio,
    avg_bert_score,
    bert_score,
]

# Some metadata to standardize huggingface datasets
dataset_mapping: dict[str | tuple[str, str], Any] = {
    "daily_dialog": {
        "data_column": "dialog",
        "data_format": "sequence",
    },
}