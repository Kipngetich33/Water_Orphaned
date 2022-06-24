function cis_page_redirect_function(clicked_button){
    var page_names = {
        'master_data':{'page':'desk#List/CIS%20Data/Report','args':{},'status':true},
        'summary_figure':{'page':'','args':{},'status':false},
        'analysis_guide_table':{'page':'desk#List/Analysis%20Guide/Report','args':{},'status':true},
        'dashboard':{'page':'dynamic_dashboard','args':{'title':'Dashboard'},'status':true},
        'pivot':{'page':'dashboard'},
        'connection_pivot':{'page':'dynamic_dashboard','args':{'title':'Connection Pivot'},'status':true},
        'billing_pivot':{'page':'dynamic_dashboard','args':{'title':'Billing Pivot'},'status':true},
        'meter_details_pivot':{'page':'dynamic_dashboard','args':{'title':'Meter Details Pivot'},'status':true},
        'meter_state_pivot':{'page':'dynamic_dashboard','args':{'title':'Meter State Pivot'},'status':true},
        'meter_problems':{'page':'dynamic_dashboard','args':{'title':'Meter Problems'},'status':true},
        'alternative_sources_of_water':{'page':'dynamic_dashboard','args':{'title':'Alternative Source of Water'},'status':true},
        'customer_satisfaction':{'page':'dynamic_dashboard','args':{'title':'Customer Satisfaction'},'status':true},
        'water_supply_pivot':{'page':'dynamic_dashboard','args':{'title':'Water Supply Pivot'},'status':true},
        'storage_tank':{'page':'dynamic_dashboard','args':{'title':'Storage Tank'},'status':true},

        // database billing dates
        'database_analysis_guide_table':{'page':'desk#List/Analysis%20Guide/Report','args':{},'status':true},
        'billing_database':{'page':'desk#List/Billing%20Database%20Detail/Report','args':{},'status':true},
        'database_analysis':{'page':'database_analysis','args':{'title':'Database Analysis'},'status':true}

    }
    // check if the page exist
    if(page_names[clicked_button.id].status){
        var origin_url = window.location.origin
        // add page
        origin_url_n_page = origin_url + `/${page_names[clicked_button.id].page}`
        base_url = new URL(origin_url_n_page)
        console.log(base_url)
        // get all the keys in the args object of the requested page
        var page_args_keys = Object.keys(page_names[clicked_button.id].args)
        // loop through the args keys adding them as url parameters
        page_args_keys.forEach(arg_key => {
            base_url.searchParams.append(arg_key, page_names[clicked_button.id].args[arg_key]);            
        });
        // finally redirect to the requested page
        location.href = base_url
    }else{
        alert("This page is under developement or does not exist")
    }

}