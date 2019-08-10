#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# extractWavLoudest

import numpy as np
import math


def extractWavLoudestArray(srcPcmNpData, desired_ms, rate, samplesTotal):
        pcmNpDataAbsArray = np.fabs(srcPcmNpData)
        needSamplesTotal = (desired_ms * rate) // 1000

        loudest_start_index = 0
        rangeMaxSumTmp = 0
        for i in range(samplesTotal - needSamplesTotal):
            thisSum = np.sum(pcmNpDataAbsArray[i : i+needSamplesTotal])
            if thisSum > rangeMaxSumTmp:
                rangeMaxSumTmp = thisSum
                loudest_start_index = i

        loudest_end_index = loudest_start_index + needSamplesTotal
        return srcPcmNpData[loudest_start_index : loudest_end_index]
        
if __name__ == "__main__":
    buffer = ''
    extractWavLoudestArray(buffer, 1000, sr, len(buffer))
