<template>
    <q-card>
        <q-card-section>
            <div class="text-h5 text-center">country level analytics</div>
        </q-card-section>
        <q-card-section>
            <div class="row">
            <div class="col-6 q-pa-sm">
                <q-card>
                <highcharts ref="chart1" class="hc" :options="chart1Options" />
                </q-card>
            </div>
            <div class="col-6 q-pa-sm">
                <q-card>
                <highcharts ref="chart4" class="hc" :options="chart4Options" />
                </q-card>
            </div>
            <div class="col-6 q-pa-sm">
                <q-card>
                <highcharts ref="chart2" class="hc" :options="chart2Options" />
                </q-card>            
            </div>
            <div class="col-6 q-pa-sm">
                <q-card>
                <highcharts ref="chart3" class="hc" :options="chart3Options" />
                </q-card>            
            </div>
            </div>
        </q-card-section>
    </q-card>
</template>

<script setup>
import { Chart as highcharts } from 'highcharts-vue'
import Highcharts from 'highcharts'
import accessibilityInit from 'highcharts/modules/accessibility'
accessibilityInit(Highcharts)

const dataSource = useState('dataSource')

const chartData = ref([])
const chartDataHistogram = ref([])

const chart1Options = computed(() => {

  var seriesData = []

  const distinctOwners = [...new Set(chartData.value.map(obj => obj.chargepointowner_name))]
  distinctOwners.forEach((specificOwner)=>{
    const filteredData = chartData.value.filter(obj => obj.chargepointowner_name === specificOwner);
    const extractedData = filteredData.map(obj => ({
      dt: obj.dt,
      util: obj.util,
      energy_consumption: obj.energy_consumption,
      charging_minutes: obj.charging_minutes
    }))
    seriesData.push(
      {
        type: 'spline',
        name: specificOwner,
        data: extractedData.map(value => value[Object.keys(extractedData[0])[1]])
      }
    )
  })
  const distinctDtValues = [...new Set(chartData.value.map(obj => obj.dt))];

  return {
    chart: {
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
      enabled: true
    },
    title: {
      text: 'utilization %',
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
    series: seriesData,
    xAxis: {
      categories: distinctDtValues,
      labels: {
        style: { fontSize: 10 },
        formatter: function () {
          return this.value.toString().substring(8, 10) + '/' + this.value.toString().substring(5, 7);
        }
      }
    }
  }
})

const chart2Options = computed(() => {

  var seriesData = []

  const distinctOwners = [...new Set(chartData.value.map(obj => obj.chargepointowner_name))]
  distinctOwners.forEach((specificOwner)=>{
    const filteredData = chartData.value.filter(obj => obj.chargepointowner_name === specificOwner);
    const extractedData = filteredData.map(obj => ({
      dt: obj.dt,
      util: obj.util,
      energy_consumption: obj.energy_consumption,
      charging_minutes: obj.charging_minutes
    }))
    seriesData.push(
      {
        type: 'areaspline',
        name: specificOwner,
        data: extractedData.map(value => value[Object.keys(extractedData[0])[3]])
      }
    )
  })
  const distinctDtValues = [...new Set(chartData.value.map(obj => obj.dt))];

  return {
    chart: {
      height: 400,
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
      enabled: true
    },
    title: {
      text: 'charging minutes',
    },
    plotOptions: {
      series: {
        stacking: 'normal',
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
    series: seriesData,
    xAxis: {
      categories: distinctDtValues,
      labels: {
        style: { fontSize: 10 },
        formatter: function () {
          return this.value.toString().substring(8, 10) + '/' + this.value.toString().substring(5, 7);
        }
      }
    }
  }
})

const chart3Options = computed(() => {
  var seriesData = []

  const distinctOwners = [...new Set(chartData.value.map(obj => obj.chargepointowner_name))]
  distinctOwners.forEach((specificOwner)=>{
    const filteredData = chartData.value.filter(obj => obj.chargepointowner_name === specificOwner);
    const extractedData = filteredData.map(obj => ({
      dt: obj.dt,
      util: obj.util,
      energy_consumption: obj.energy_consumption,
      charging_minutes: obj.charging_minutes
    }))
    seriesData.push(
      {
        type: 'areaspline',
        name: specificOwner,
        data: extractedData.map(value => value[Object.keys(extractedData[0])[2]])
      }
    )
  })
  const distinctDtValues = [...new Set(chartData.value.map(obj => obj.dt))];

  return {
    chart: {
      height: 400,
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
      enabled: true
    },
    title: {
      text: 'energy consumption',
    },
    plotOptions: {
      series: {
        stacking: 'normal',
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
    series: seriesData,
    xAxis: {
      categories: distinctDtValues,
      labels: {
        style: { fontSize: 10 },
        formatter: function () {
          return this.value.toString().substring(8, 10) + '/' + this.value.toString().substring(5, 7);
        }
      }
    }
  }
})


const chart4Options = computed(() => {
  return {
    chart: {
      height: 400,
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
      text: 'location count / utilization',
    },
    plotOptions: {
      series: {
        pointWidth: 30,
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
        name: 'utilization_distribution',
        color: '#0f0f0f',
        data: chartDataHistogram.value.map(value => value[Object.keys(chartDataHistogram.value[0])[1]])
      }
    ],
    xAxis: {
      categories: ['0-2%','2-4%','4-6%','6-8%','8-10%','10-12%','12-14%','14-16%','>16%'],
      labels: {
        style: { fontSize: 10 },
      }
    }
  }
})

onMounted(async () => {
  const { data: data1 } = await useFetch('http://34.171.207.247:5000/getAllStats/'+(dataSource.value == 'CNROpt' ? '0':'1'), {
    onResponse({ response }) {
      chartData.value = response._data
    }
  })
  const { data: data2 } = await useFetch('http://34.171.207.247:5000/getAllStatsHistogram/'+(dataSource.value == 'CNROpt' ? '0':'1'), {
    onResponse({ response }) {
      chartDataHistogram.value = response._data
    }
  })

})

</script>