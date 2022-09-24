#!/bin/bash

echo "What is your phone number" | festival --tts

response=$(./speech_to_text)

echo "$response"
