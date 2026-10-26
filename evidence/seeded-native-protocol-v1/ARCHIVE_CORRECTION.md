# Archive packaging correction before native execution

The first tag evidence-seeded-native-protocol-v1-2026-10-26 points to runner source
847540ed8fb3e22d8f4f70e9fbeb7ca956db7e0d, without the staged payload. A staged
whitespace check reported original DATASET_CARD.md trailing whitespace and stopped
the payload commit; a separate command incorrectly proceeded to tag/push HEAD.
Tag object b0cf08510d62092281d9b6f3db99f1a3491b2ee0 remains unchanged. No native
execution occurred. The corrected v2 tag contains the unchanged staged payload and
this correction. Original card whitespace is retained, not silently normalized.
Manifest, comparison, inputs, support and scientific settings are unchanged.
