var dashboard_keys1 = ['Connection Status vs Account Known']

var all_dashboard_keys = { 
    'en':['Customer Connected to WSP',
        'Account Details Known',
        // 'Customer Willing to be Connected',
        // 'Potential Customers Connectable',
        // 'Reasons Customer is not Connected to WSP',
        'Connection Status',
        'Disconnection Duration',
        'Connection Status vs Account Known',
        'Billing Status',
        'Billing Status vs Connection Status',
        'Frequency of Bill Delivery',
        'Frequency of Bill Delivery VS Account Status',
        'How Often Do You Recieve Water',
        'Reasons not Billed',
        'Daily Hours of Supply',
        'Last Time to Recieve Water',
        // 'Alternative Sources of Water',
        'Water Meter Connected',
        'Meter Status',
        'Meter Status Vs Connection Status',
        'Meter Material',
        'Meter Location',
        'Meter Settlement',
        'Meter Flow Direction',
        'Meter Read Monthly',
        'Meter Class',
        'Meter State',
        // 'Meter Location Inside The Premises',
        'Meter Brand',
        'Pipe Material',
        // 'Meter Problems',
        'Location of Storge Tank',
        'Type of Sanitation',
        'Type of Pit Latrine',
        'Type VS Category of Pit Latrine',
        'Type of Septic',
        'Onsite Category',
        'Type VS Category of Setptic',
        'Housing Type',
        'Premise Type',
        'Domestic Housing Type',
        // 'Customer Satisfaction',
    ],
    'pt':['Cliente conectado ao fornecedor de serviços de água',
        'Detalhes da conta conhecidos',
        // 'Customer Willing to be Connected',
        // 'Potential Customers Connectable',
        // 'Reasons Customer is not Connected to WSP',
        'Status da conexão',
        'Duração da Desconexão',
        'Status da conexão versus conta conhecida',
        'Status de cobrança',
        'Status de cobrança versus status de conexão',
        'Frequência de entrega de faturas',
        'Frequência de entrega de faturas versus status da conta',
        'Com que frequência você recebe água',
        'Razões não faturadas',
        'Horas diárias de abastecimento',
        'Última vez para receber água',
        // 'Alternative Sources of Water',
        'Medidor de água conectado',
        'Status do medidor',
        'Status do medidor versus status da conexão',
        'Material do Medidor',
        'Localização do medidor',
        'Liquidação do medidor',
        'Direção do Fluxo do Medidor',
        'Medidor lido mensalmente',
        'Classe de Medidor',
        'Estado do Medidor',
        // 'Meter Location Inside The Premises',
        'Marca do Medidor',
        'Material de Tubulação',
        // 'Meter Problems',
        'Localização do tanque Storge',
        'Tipo de Saneamento',
        'Tipo de latrina de fossa',
        'Tipo versus categoria de latrina de fossa',
        'Tipo de séptica',
        'Categoria no local',
        'Tipo versus categoria de setptic',
        'Tipo de Habitação',
        'Tipo de premissa',
        'Tipo de Habitação Doméstica',
        // 'Customer Satisfaction',
    ],
}

var pivot_dashboard_keys ={
    'Dashboard':all_dashboard_keys,
    'Customer Pivot':['Customer Connected to WSP',
            'Account Details Known',
            'Customer Willing to be Connected',
        ],
    'Connection Pivot':['Connection Status',
            'Disconnection Duration',
            'Connection Status vs Account Known'
        ],
    'Billing Pivot':['Billing Status',
            'Billing Status vs Connection Status',
            'Frequency of Bill Delivery',
            'Frequency of Bill Delivery VS Account Status',
            'How Often Do You Recieve Water',
            'Reasons not Billed',
        ],
    "Meter Details Pivot":['Water Meter Connected',
            'Meter Location',
            'Meter Status',
            'Meter Settlement',
            'Meter Material',
            'Meter Flow Direction',
            'Meter Read Monthly',
        ],
    "Meter State Pivot":[
            'Meter State',
            'Pipe Material',
            'Meter Class',
            'Meter Brand',
        ],
    'Meter Problems':[
            'Meter Problems', 
        ],
    'Alternative Sources of Water':[
        'Alternative Sources of Water',
    ],
    'Sanitation Pivot':[
        'Type of Sanitation',
        'Type of Pit Latrine',
        'Type VS Category of Pit Latrine',
        'Type of Septic',
        'Onsite Category',
        'Type VS Category of Setptic',
    ],
    'Storage Tank':[
        'Location of Storge Tank',
    ],
    'Water Supply Pivot':[
        'How Often Do You Recieve Water',
        'Daily Hours of Supply',
    ],
    'Customer Satisfaction':['Customer Satisfaction']

}

// function that add or remove the loader on page
function add_remove_loader(action){
    if(action== true){
        var loader_div = document.createElement("div");
        loader_div.setAttribute('class',"loader")
        loader_div.setAttribute('id',"loader")
        document.getElementById("dashboard_cards_section").appendChild(loader_div)
    }else{
        var elem = document.getElementById("loader");
        elem.parentNode.removeChild(elem);
    }
}

// function that gets parameters passed to the url 
function getUrlParameter(name){
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

// function that adds certain text to a given section/id
function add_text_to_doc(text_to_add,where_to_add){
    if(text_to_add){
        var user_name = document.createTextNode(text_to_add);
        document.getElementById(where_to_add).appendChild(user_name)
    }
}

function create_dashboard_card(chart_title,chart_id){
    var dashboard_card_div = document.createElement("div");
    dashboard_card_div.setAttribute('class','card')
    dashboard_card_div.setAttribute('style','margin:10px;padding:10px;')
    // add card header
    var card_header = document.createElement("h5");
    card_header.innerHTML = chart_title
    card_header.setAttribute('class','card-header')
    dashboard_card_div.appendChild(card_header)
    // create card
    var card_body_div = document.createElement("div");
    card_body_div.setAttribute('class','card-body')
    card_body_div.setAttribute('style','text-align:center;')
    // create row to hold the card body content
    var card_body_row = document.createElement("div");
    card_body_row.setAttribute('class','row')
    // create the chart body div col-md-8
    var canvas_holder_div = document.createElement("div");
    canvas_holder_div.setAttribute('class','col-md-8')
    // create a chart canvas to append to canvas holder div
    var canvas = document.createElement("canvas");
    canvas.setAttribute('style','margin:10px;max-height:275px;')
    canvas.setAttribute('id',chart_id)
    canvas_holder_div.appendChild(canvas)
    // create the chart labels div col-md-4
    var canvas_labels_div = document.createElement("div");
    canvas_labels_div.setAttribute('class','col-md-4')
    canvas_labels_div.setAttribute('id',chart_id+"_labels")
    canvas_labels_div.setAttribute('style','padding-top:20px;')
    // append to main
    card_body_row.appendChild(canvas_holder_div)
    card_body_row.appendChild(canvas_labels_div)
    card_body_div.appendChild(card_body_row)
    dashboard_card_div.appendChild(card_body_div)
    // add to html document
    document.getElementById("dashboard_cards_section").appendChild(dashboard_card_div)
}

var data_labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
var chart_label = '# of Votes'
var chart_data = [12, 19, 3, 5, 2, 3]
var chart_backgroundColor = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgb(224, 248, 252)',
    'rgb(227,247,234)',
    'rgb(202,299,194)',
    'rgb(249,245,194)',
    'rgb(242,201,169)',
    'rgb(169,224,242)',
]
var chart_borderColor = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgb(4, 139, 249)',
    'rgb(4,247,83)',
    'rgb(37,247,4)',
    'rgb(226,208,11)',
    'rgb(229,104,9)',
    'rgb(10,157,206)',
]

// dynamic charting function that creates charts based on parsed values
function charting_function(chart_id,chart_type,data_labels,chart_datasets){
    var ctx = document.getElementById(chart_id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: chart_type,
        data: {
            labels:data_labels ,
            datasets:chart_datasets
        },
    });
}

// function that create visible data labels for each chart
function create_labels_values(chart_id,data_labels,list_of_complete_datasets){
    var labels_div_name = chart_id + "_labels"
    var index_count = 0

    // loop through the data labels
    data_labels.forEach(function(current_data_label){
        // check if data set is stacked
        if(list_of_complete_datasets.length == 1){
            // data labels div
            var current_data_label_element = document.createElement("h6");
            current_data_label_element.setAttribute('style','text-align:left;margin-top:10px;')
            var current_data_label_icon = document.createElement("i");
            current_data_label_icon.setAttribute('class','fa fa-square')
            current_data_label_icon.setAttribute('aria-hidden',true)
            // set values
            var dataset_color  = list_of_complete_datasets[0].backgroundColor[index_count]
            current_data_label_element.innerHTML = `<i class="fa fa-square" aria-hidden="true" style="color:${dataset_color};"></i>`
            current_data_label_element.innerHTML += ' '
            current_data_label_element.innerHTML += current_data_label
            current_data_label_element.innerHTML += ' -'
            current_data_label_element.innerHTML += list_of_complete_datasets[0].data[index_count]

            // add to counter
            index_count += 1
            document.getElementById(labels_div_name).appendChild(current_data_label_element)
        }else if(list_of_complete_datasets.length > 1){
            // create labels for stacked data
            var current_data_label_element = document.createElement("h5");
            current_data_label_element.innerHTML = current_data_label
            current_data_label_element.setAttribute('style','font-weight:bold;text-align:left')
            // append to labels div
            document.getElementById(labels_div_name).appendChild(current_data_label_element)
            // create labels for each values in the stacked chart
            list_of_complete_datasets.forEach(function(current_sub_data_label){
                var single_data_label_element = document.createElement("h6");
                single_data_label_element.setAttribute('style','text-align:left;margin-top:10px;')
                var single_data_label_icon = document.createElement("i");
                single_data_label_icon.setAttribute('class','fa fa-square')
                single_data_label_icon.setAttribute('aria-hidden',true)
                // set values
                var single_dataset_color  = current_sub_data_label.backgroundColor
                single_data_label_element.innerHTML = `<i class="fa fa-square" aria-hidden="true" style="color:${single_dataset_color};"></i>`
                single_data_label_element.innerHTML += ' '
                single_data_label_element.innerHTML += current_sub_data_label.label
                single_data_label_element.innerHTML += ' -'
                single_data_label_element.innerHTML += current_sub_data_label.data[index_count]
                document.getElementById(labels_div_name).appendChild(single_data_label_element)
            })
            // add to counter
            index_count += 1
        }

        
    })
}

function main(dashboard_data){
    var correct_language = dashboard_data['language']
    // get parameters parsed in the url
    var page_title = getUrlParameter('title')
    // add title and breadcrumb title
    add_text_to_doc(page_title,'cis_title')
    add_text_to_doc(page_title,'breadcrumb_title')
    // check if title is defined
    if(page_title){
        var dashboard_keys = all_dashboard_keys[correct_language] 
    }else{
        var dashboard_keys = pivot_dashboard_keys[page_title]
    }
    // loop through dashboard_data to determine dashboards to display
    dashboard_keys.forEach(function(dashboard_key){
        // add a try statement to ensure errors do not prevent other dashboards from showing
        try{
            // get required key values for the charting function
            var chart_id = dashboard_data[dashboard_key].chart_settings.chart_id
            var chart_type = dashboard_data[dashboard_key].chart_settings.chart_type
            var data_labels = []
            var chart_data = []
            var all_datasets = {}
            var list_of_complete_datasets = []
            stacked_dataset = false
            // create chart data and data labels
            Object.keys(dashboard_data[dashboard_key]).forEach(function(chart_value){
                if(chart_value != 'chart_settings'){
                    var current_chart_value = dashboard_data[dashboard_key][chart_value]
                    data_labels.push(chart_value)
                    // check if the given type is an object meaning stacked data
                    if(typeof current_chart_value == 'object'){
                        stacked_dataset = true
                        // loop through the keys to create datasets
                        Object.keys(current_chart_value).forEach(function(chart_value_key){
                            if(Object.keys(all_datasets).includes(chart_value_key)){
                                all_datasets[chart_value_key].push(current_chart_value[chart_value_key])
                            }else{
                                all_datasets[chart_value_key] = []
                                all_datasets[chart_value_key].push(current_chart_value[chart_value_key])
                            }
                        })
                    }else{
                        // the chart data is not stacked
                        stacked_dataset = false
                        chart_data.push(dashboard_data[dashboard_key][chart_value])
                    }
                }
            })
            // now create complete datasets
            if(stacked_dataset){
                Object.keys(all_datasets).forEach(function(single_dataset_key){
                    list_of_complete_datasets.push({
                            label:single_dataset_key,
                            backgroundColor:chart_backgroundColor[list_of_complete_datasets.length],
                            borderColor:chart_backgroundColor[list_of_complete_datasets.length],
                            data: all_datasets[single_dataset_key],
                        }
                    )
                })
            }else{
                list_of_complete_datasets.push({
                    backgroundColor:chart_backgroundColor,
                    borderColor: chart_borderColor,
                    data: chart_data,
                }
            )
            }
    
            // create a dashboard card
            create_dashboard_card(dashboard_key,chart_id)
            charting_function(chart_id,chart_type,data_labels,list_of_complete_datasets)
            create_labels_values(chart_id,data_labels,list_of_complete_datasets)
        }catch(err) {
            console.log("error occured")
            console.log(err)
        }
    })
}

// function that pulls cis data from database
function pull_cis_data(){
    // add the loader to page
    add_remove_loader(true)
    var url = "/api/method/water.templates.pages.dynamic_dashboard.filter_cis_data_for_chart"

    // ajax calls to response
    $.ajax({
        url:url,
        async: true,
        dataType: 'json',
        success: function (response) {
            // remove loader from the page
            add_remove_loader(false)
            if(response.message){
                if(response.message.status){
                    // call the main function to build the dashbaord
                    main(response.message)
                }else{
                    alert(response.message.message)
                    // location.href = '/cis_analysis'
                }
            }else{
                alert("No CIS Data was found for this Dashboard")
                location.href = '/cis_analysis'
            } 
        },
        cache: false,
    });
}
pull_cis_data()