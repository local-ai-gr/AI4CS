<template>
  <q-card class="q-ma-lg" :style="{ backgroundColor: props.stationData.candidate== undefined ? 'white' : 'LightGoldenRodYellow' }">
    <q-card-section>
      <div style="width: 320px;height:100px">
        <img class="tw-rounded-lg tw-h-auto tw-max-w-full"
          :src="'https://maps.googleapis.com/maps/api/streetview?size=320x100&location=' + props.stationData.lat + ',' + props.stationData.lon + '&fov=120&heading=70&pitch=0&zoom=15&key=AIzaSyDqpZWfYPvfKtilFrzArr_3Pqt6v5TpPSs'" />
      </div>
    </q-card-section>
    <q-card-section class="q-py-none">
      <div class="row no-wrap items-center">
        <div class="col text-h4">{{ props.stationData.location_friendlyname }}</div>
      </div>
    </q-card-section>
    <q-card-section class="q-py-none">
      <div class="row justify-evenly">
        <div class="col text-left"><span class="text-h5">{{ Math.round(props.stationData.utilization, 0) }}%</span> <span
            class="text-h6 text-grey">utilization</span> <span v-if="props.stationData.candidate!= undefined">(estimated)</span></div>
        <div v-if="props.stationData.candidate== undefined" class="col -h4 text-right"><span class="text-h6 text-grey">connectors</span><span class="text-h5">{{
          props.stationData.number_of_connectors }}</span></div>
      </div>
    </q-card-section>
    <div v-if="props.stationData.candidate== undefined">
      <q-card-section>
      <q-btn-toggle flat
      v-model="chartMetric"
      toggle-color="primary"
      size="md"
      :options="[
        {label: 'utilization', value: 'utilization'},
        {label: 'energy', value: 'energy'}
      ]"
    />
    <q-checkbox
      v-model="showPrediction"
      checked-icon="update"
      unchecked-icon="history_toggle_off"
      label="forecast"
      color="red"
    />
    </q-card-section>
    <q-card-section class="q-py-none" v-if="$q.screen.height > 820">
      <highcharts ref="chart2" class="hc" :options="chart2Options" />
      <highcharts ref="chart1" class="hc" :options="chart1Options" />
    </q-card-section>
    <q-card-section class="q-pt-none" v-if="$q.screen.height <= 820">
      <q-tabs v-model="utilTabs" dense class="text-grey" active-color="primary" indicator-color="primary" align="justify"
        narrow-indicator>
        <q-tab name="daily" label="Daily" />
        <q-tab name="hourly" label="Hourly" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="utilTabs" animated>
        <q-tab-panel name="daily">
          <highcharts ref="chart2" class="hc" :options="chart2Options" />
        </q-tab-panel>
        <q-tab-panel name="hourly">
          <highcharts ref="chart1" class="hc" :options="chart1Options" />
        </q-tab-panel>
      </q-tab-panels>
    </q-card-section>
    </div>
  </q-card>
</template>

<script setup>
import { Chart as highcharts } from 'highcharts-vue'
import Highcharts from 'highcharts'
import accessibilityInit from 'highcharts/modules/accessibility'
accessibilityInit(Highcharts)

import { useQuasar } from 'quasar'
const $q = useQuasar()

const dataSource = useState('dataSource')

const chartMetric = ref('utilization')
const utilTabs = ref('daily')
const showPrediction = ref(false)



const props = defineProps(['stationData'])

const chart1Data = ref([])
const chart2Data = ref([])

const chart1Options = computed(() => {
  return {
    chart: {
      height: 230,
      zooming: {
        type: 'x'
      },
      style: {
        fontFamily: 'Titillium Web'
      }
    },
    credits: {
      enabled: false
    },
    legend: {
      enabled: false
    },
    title: {
      text: 'hourly '+chartMetric.value,
    },
    plotOptions: {
      series: {
        pointWidth: 3,
        stickyTracking: false,
        label: {
          connectorAllowed: false
        },
        marker: {
          enabled: false
        }
      }
    },
    yAxis: {
      title: { text: undefined }
    },
    series: [
      {
        type: 'column',
        name: chartMetric.value,
        data: chart1Data.value.map(value => {
          const yValue = value[Object.keys(chart1Data.value[0])[1]];
          const colorValue = value[Object.keys(chart1Data.value[0])[2]];
          const color = colorValue==0 ? '#2caffe' : 'red'
          return {
            y: yValue,
            color: color,
          };
        })
      }
    ],
    xAxis: {
      categories: chart1Data.value.map(value => value[Object.keys(chart1Data.value[0])[0]]),
      labels: {
        style: { fontSize: 10 },
        formatter: function () {
          return this.value.toString().substring(8, 10) + '/' + this.value.toString().substring(5, 7) + ' ' + this.value.toString().substring(11, 13);
        }
      }
    }
  }
})


const chart2Options = computed(() => {

  return {
    chart: {
      height: 230,
      zooming: {
        type: 'x'
      },
      style: {
        fontFamily: 'Titillium Web'
      }
    },
    credits: {
      enabled: false
    },
    legend: {
      enabled: false
    },
    title: {
      text: 'daily '+chartMetric.value,
    },
    plotOptions: {
      series: {
        pointWidth: 4,
        stickyTracking: false,
        label: {
          connectorAllowed: false
        },
        marker: {
          enabled: false
        }
      }
    },
    yAxis: {
      title: { text: undefined }
    },
    series: [
      {
        type: 'column',
        name: chartMetric.value,
        data: chart2Data.value.map(value => {
          const yValue = value[Object.keys(chart2Data.value[0])[1]];
          const colorValue = value[Object.keys(chart2Data.value[0])[2]];
          const color = colorValue==0 ? '#2caffe' : 'red'
          return {
            y: yValue,
            color: color,
          };
        })
      }
    ],
    xAxis: {
      categories: chart2Data.value.map(value => value[Object.keys(chart2Data.value[0])[0]]),
      labels: {
        style: { fontSize: 10 },
        formatter: function () {
          return this.value.toString().substring(8, 10) + '/' + this.value.toString().substring(5, 7);
        }
      }
    }
  }
})

onMounted(async () => {
  getChartData('utilization', false)
})

async function getChartData(metric, prediction) {
  const { data: data1 } = await useFetch('http://34.171.207.247:5000/getStationStatsHour/'+(dataSource.value == 'CNROpt' ? '0':'1')+'/' + props.stationData.location_id+'/'+metric+'/'+prediction, {
    onResponse({ response }) {
      chart1Data.value = response._data
    }
  })
  const { data: data2 } = await useFetch('http://34.171.207.247:5000/getStationStatsDay/'+(dataSource.value == 'CNROpt' ? '0':'1')+'/'+ props.stationData.location_id+'/'+metric+'/'+prediction, {
    onResponse({ response }) {
      chart2Data.value = response._data
    }
  })
}

watch(chartMetric, async (newChartMetric)=> {
  getChartData(newChartMetric, showPrediction.value)
})

watch(showPrediction, async (newPrediction)=> {
  getChartData(chartMetric.value, newPrediction)
})

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web&display=swap');
</style>