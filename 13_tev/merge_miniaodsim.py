import FWCore.ParameterSet.Config as cms

process = cms.Process("Merge")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_1.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_2901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_3901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_4901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_5901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_6901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_7901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8001.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8101.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8201.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8301.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8401.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8501.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8601.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8701.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8801.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_8901.root',
'file:eos/cms/store/user/anlevin/data/MINIAOD/ttbar_13_tev/step5_output_901.root')
)
process.Merged = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('Merged.root'),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    logicalFileName = cms.untracked.string('/store/mc/Spring14miniaod/TToBLNu_tW-channel-DR-EMu_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_POSTLS170_V5-v2/30000/Merged.root')
)


process.outputPath = cms.EndPath(process.Merged)


process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck")


process.Timing = cms.Service("Timing",
    summaryOnly = cms.untracked.bool(True)
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)


