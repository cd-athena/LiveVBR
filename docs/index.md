# Index

## Introduction

Adaptive live video streaming applications utilize a predefined collection of bitrate-resolution pairs, known as a bitrate ladder, for simplicity and efficiency, eliminating the need for additional run-time to determine the optimal pairs during the live streaming session.
These applications do not incorporate two-pass encoding methods due to increased latency.
However, an optimized bitrate ladder could result in lower storage and delivery costs and improved Quality of Experience (QoE).
For each segment, perceptually aware bitrate-resolution-CRF triples are predicted by LiveVBR.


## About LiveVBR

The primary objective of LiveVBR is a two-pass cVBR encoding scheme with a content-adaptive, JND-aware, online bitrate ladder prediction optimized for adaptive live streaming applications.
The minimum and maximum encoding bitrates, the maximum quality level, and the target average JND function are considered as inputs to the scheme.
Moreover, the encoder/codec used, is input to the scheme to ensure that the bitrate ladder is generated for the corresponding encoder.
Based on the video complexity features (extracted by VCA) and the input parameters, bitrate-resolution-CRF triples are predicted.
The adjacent points of the bitrate ladder are envisioned to have a perceptual quality difference of one JND.
Although reducing the overall storage needed to store the representations, LiveVBR is expected to improve the overall compression efficiency of the bitrate ladder encoding.

LiveVBR is available as an open source library, published under the GPLv3 license.

![ATHENA](https://athena.wp.itec.aau.at/wp-content/uploads/sites/12/2020/02/athena-logo-notagline-300x51.png)
