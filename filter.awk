#!/usr/bin/awk -f
## Filters MASS file from wrong output data (to be done AFTER reprocessing)
##
## Description: suppress output of ATR-lines in following cases:
## - Large background-to-flux ratio in D-aperture (>MAX_BG_F_D) 
## - Low D-flux (<MIN_D) or large D-flux error (>MAX_E_D)
## - Large Absolute FSEE error (>MAX_AE_FSEE)
## - Large Chi2 in restored profiles (>MAX_CHI2)
## Parameters: see above in parentheses
## Use as: filter.awk [par1=val1 [par2=val2] [..]] mass-file  >result-file
BEGIN{
	# flag to mark good data:
	good = 0; backd=1; fluxd=1; tgood=0;
	MAX_BG_F_D = 0.03
	MAX_CHI2 = 100
	MAX_D = 10000
	MIN_D = 100
	MAX_E_D = 0.01
	MAX_AE_FSEE = 0.2
	nfilt = 0
	utreject = 0
}

NR==1 {
	print "## ==== FILTER out on: BG/D>"MAX_BG_F_D" D<"MIN_D" D>"MAX_D" e_D>"MAX_E_D\
	" Fsee*e_Fsee>"MAX_AE_FSEE" Chi2>"MAX_CHI2
}

# Register background in D:
$1=="P" &&  substr($4,12,10)=="Background" {
	backd = $8
}

# Register flux in D and compute "good" by D-flux:
$1=="F" {
	fluxd = $10
	e_fluxd = $11
	if (fluxd==0) fluxd=1;
	good = (backd/fluxd<MAX_BG_F_D && fluxd>MIN_D && fluxd<MAX_D && e_fluxd<MAX_E_D)
}

# Print non-final-result-lines as is:
$1~/[OP#MCFULDIJ>].*/ && !($1=="##" && $0~/FILTER/) {print}

substr($1,1,1)~/[ATRW]/ {
	if ($1=="A") good = (good && $4*$5<MAX_AE_FSEE)
	if ($1=="T") good = (good && $6<MAX_CHI2)
	if ($1=="W") good = (good && $0!~/nan/ && $0!~/inf/)
	if (!good) {
		printf "## FILTER out:"
		if (utreject!=$3) {
			# we count only UTmid moments with any rejected results:
			nfilt++; 
			utreject = $3
		}
	}
	print
}

END{
	print "## FILTER out "nfilt" observations" 
}
