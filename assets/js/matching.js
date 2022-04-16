#!/usr/bin/node

async function getMatchedMigrantWorker(donationID) {
    let response = await fetch("http://127.0.0.1:5003/matchingAlgorithm/" + donationID)
    let responseJson = await response.json()

    if (responseJson.code == 200) {
        return responseJson.finalMW
    } else {
        alert(responseJson.message)
    }
}
