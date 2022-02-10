##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Cleaner                                                 #
#                                                            #
##############################################################
import os

bashCommand = "bash bash_scripts/cleaner.sh -i medical_notes -o cleaned_medical_notes"
os.system(bashCommand)