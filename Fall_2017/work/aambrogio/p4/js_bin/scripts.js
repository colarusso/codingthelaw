function fedpov(house,income,percentage){
// Determines if your income is less than or equal to 
// a percentage of the federal poverty guidlines for 
// the contiguous United States.
	
	var line = NaN;
	
	if (house == 1) {
		line = 12060;
	} else if (house == 2) {
		line = 16240;
	} else if (house == 3) {
		line = 20420;
	} else if (house == 4) {
		line = 24600;
	} else if (house == 5) {
		line = 28780;
	} else if (house == 6) {
		line = 32960;
	} else if (house == 7) {
		line = 37140;
	} else if (house == 8) {
		line = 41320;
	} else if (house > 8) {
		line = 41320 + (house-8)*4180;
	}
	
	if (income <= (line*(percentage/100))) {
		return true;
	} else {
		return false;
	}
}


function sixmedinc(house,income){
// Determines if your income is less than or equal to 
// 60% of the median income for Mass. 
	
	var line = NaN;
	
	if (house == 1) {
		line = 34380;
	} else if (house == 2) {
		line = 16240;
	} else if (house == 3) {
		line = 20420;
	} else if (house == 4) {
		line = 24600;
	} else if (house == 5) {
		line = 28780;
	} else if (house == 6) {
		line = 32960;
	} else if (house == 7) {
		line = 37140;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else if (house == 8) {
		line = 41320;
	} else {
		alert("Note: Cannot accept household of more that 17.");
	}
	
	if (income <= line) {
		return true;
	} else {
		return false;
	}
}
