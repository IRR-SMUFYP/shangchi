#!/usr/bin/node

async function getMatchedMigrantWorker(donationID) {
    let response = await fetch("http://ec2-13-250-122-219.ap-southeast-1.compute.amazonaws.com:5003/matchingAlgorithm/" + donationID)
    let responseJson = await response.json()

    if (responseJson.code == 200) {
        return responseJson.finalMW
    } else {
        alert(responseJson.message)
    }
}
