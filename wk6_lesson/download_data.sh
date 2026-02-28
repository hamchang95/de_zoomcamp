set -e

TAXI_TYPE=$1
YEAR=$2

URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


for MONTH in {01..12}; do
    #FMONTH = `printf "%02d" ${Month}` 
    URL="${URL_PREFIX}/${TAXI_TYPE}/${TAXI_TYPE}_tripdata_${YEAR}-${MONTH}.csv.gz"

    LOCAL_PREFIX="data/raw/${TAXI_TYPE}/${YEAR}/${MONTH}"
    LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}_${MONTH}.csv.gz"
    LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

    echo "downloading ${URL} to ${LOCAL_PATH}"
    mkdir -p ${LOCAL_PREFIX}
    wget2 ${URL} -O ${LOCAL_PATH}

done 