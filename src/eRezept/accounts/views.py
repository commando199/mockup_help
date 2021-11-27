from __future__ import print_function
import re
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, shipping_optimized
from django.contrib import messages
from io import BytesIO
import numbers
from geopy import distance
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.template.loader import get_template
from django.views import View
import folium
import geopy.distance
from . import getroute
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from xhtml2pdf import pisa
from .decorators import unauthenticated_user
from .decorators import arzt_only, apotheke_only, praxis_only
from .forms import CustomUserCreationForm
import _datetime
from .forms import CustomApothekeCreationForm
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from .models import ShippingInfo
from .authenticator import authenticate_praxis, authenticate_admin
from .models import Praxis
import json
import datetime
from django.shortcuts import render, redirect
from .forms import CustomPraxisCreationForm, ShippingInfoForm




def showmap(request):
    return render(request,'showmap.html')

def showroute(request):
    figure = folium.Figure()
    all_shippings = ShippingInfo.objects.all()
    T = []
    info = []
    for i in range(len(all_shippings)):
        info.append([all_shippings[i].city_sender,all_shippings[i].city_receiver])

    for i in range(len(all_shippings)):
        T.append([all_shippings[i].longitude_sender,all_shippings[i].latitude_sender,all_shippings[i].longitude_receiver,all_shippings[i].latitude_receiver])

    lat1, long1, lat2, long2 = float(41.40338), float(2.17403), float(46.592551), float(7.753058)
    route = getroute.get_route(long1, lat1, long2, lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])],
                   tooltip='This tooltip will appear on hover',
                   zoom_start=5)
    m.add_to(figure)

    counter = 0
    for x in range(len(T)):
        counter +=1
        route1 = getroute.get_route(T[x][0], T[x][1], T[x][2], T[x][3])
        if counter%9==0:
            folium.PolyLine(route1['route'], weight=8, color='black', opacity=0.5,popup=info[x][0] + "-" +info[x][1]).add_to(m)
        elif counter%9==1:
            folium.PolyLine(route1['route'], weight=8, color='purple', opacity=0.4,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==2:
            folium.PolyLine(route1['route'], weight=8, color='darkgreen', opacity=0.4,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==3:
            folium.PolyLine(route1['route'], weight=8, color='pink', opacity=0.6,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==4:
            folium.PolyLine(route1['route'], weight=8, color='red', opacity=0.4,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==5:
            folium.PolyLine(route1['route'], weight=8, color='blue', opacity=0.4,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==6:
            folium.PolyLine(route1['route'], weight=8, color='gray', opacity=0.6,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==7:
            folium.PolyLine(route1['route'], weight=8, color='lightblue', opacity=0.8,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        elif counter%9==8:
            folium.PolyLine(route1['route'], weight=8, color='darkred   ', opacity=0.4,popup=info[x][0] + "-" + info[x][1]).add_to(m)
        else:
            folium.PolyLine(route1['route'], weight=8, color='orange', opacity=0.7,popup=info[x][0] + "-" + info[x][1]).add_to(m)

        folium.Marker(location=route1['start_point'],opacity=0.7,clustered_marker=True, icon=folium.Icon(icon='play', color='green',fill=True)).add_to(m)
        folium.Marker(location=route1['end_point'], opacity=0.7, clustered_marker=True,icon=folium.Icon(icon='stop', color='red',fill=True)).add_to(m)

    figure.render()
    context={'map':figure}
    return render(request,'showroute.html',context)





def create_data_model():
    """Stores the data for the problem."""
    data = {}
    T = []
    info = []
    data['distance_matrix'] = []
    all_shippings = ShippingInfo.objects.all()
    for i in range(len(all_shippings)):
        info.append([all_shippings[i].city_sender, all_shippings[i].city_receiver])

    T.append([51.756, 19.456])
    for i in range(len(all_shippings)):
        T.append(
            [all_shippings[i].latitude_sender, all_shippings[i].longitude_sender])
        T.append(
            [all_shippings[i].latitude_receiver, all_shippings[i].longitude_receiver])
    for y in range(len(T)):
        new = []
        for x in range(len(T)):
            new.append(int(distance.distance(T[y], T[x]).km))
        data['distance_matrix'].append(new)
    print(data['distance_matrix'])
    data['demands'] = []
    new=[]
    data['demands'].append(0)
    for x in all_shippings:
        data['demands'].append(x.weight)
        data['demands'].append(x.weight)

    print(data['demands'])


    data['pickups_deliveries'] = []
    i = 1
    while i < len(T):
        new = []
        new.append(i)
        new.append(i+1)
        i+=2
        data['pickups_deliveries'].append(new)
    print(data['pickups_deliveries'])



    data['vehicle_capacities'] = [12000, 12000, 12000]
    data['num_vehicles'] = 3
    data['depot'] = 0

    return data



def optimize(request):
    context={}

    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        100000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Define Transportation Requests.
    for input in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(input[0])
        delivery_index = manager.NodeToIndex(input[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        routing.solver().Add(distance_dimension.CumulVar(pickup_index) <= distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.solution_limit = 1
    # search_parameters.time_limit.seconds = 300

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console

    """Prints assignment on console."""
    total_distance = 0
    routes = []
    routes_for_id = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        new = []
        new_for_id = []
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            new.append(manager.IndexToNode(index))
            new_for_id.append(manager.IndexToNode(index))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        new.append(0)
        routes.append(new)
        routes_for_id.append(new_for_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))

        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance

    T = []
    ids = []
    all_shippings = ShippingInfo.objects.all()
    T.append([51.756, 19.456,0])
    for i in range(len(all_shippings)):
        ids.append(all_shippings[i].id)
        T.append(
            [all_shippings[i].latitude_sender, all_shippings[i].longitude_sender,all_shippings[i].id])
        T.append(
            [all_shippings[i].latitude_receiver, all_shippings[i].longitude_receiver,all_shippings[i].id])

    figure = folium.Figure()
    lat1, long1, lat2, long2 = float(41.40338), float(2.17403), float(46.592551), float(7.753058)
    route = getroute.get_route(long1, lat1, long2, lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])],
                   tooltip='This tooltip will appear on hover',
                   zoom_start=5)
    m.add_to(figure)

    new_routes = []

    for i in range(len(routes_for_id)):
        new = []
        for j in range(len(routes_for_id[i])):
            new.append(T[routes_for_id[i][j]][2])
        new_routes.append(new)

    print(new_routes)



    colors = ['blue','green','red','orange','black','pink','darkgreen']
    for i in range(len(routes)):
        for j in range (len(routes[i])-1):
            route1 = getroute.get_route(T[routes[i][j]][1],T[routes[i][j]][0],  T[routes[i][j+1]][1],T[routes[i][j+1]][0])
            folium.PolyLine(route1['route'], weight=8, color=colors[i], opacity=0.5).add_to(m)
            folium.Marker(location=route1['start_point'], opacity=0.7, clustered_marker=True).add_to(m)
        #route1 = getroute.get_route(T[len(routes[i])][0],T[len(routes[i])][0],T[0][0], T[0][1])
        #folium.PolyLine(route1['route'], weight=8, color=colors[i], opacity=0.5).add_to(m)


    figure.render()
    context = {'map': figure}

    return render(request, 'accounts/optimize.html',context)








def showroute1(request):
    figure = folium.Figure()
    all_shippings = shipping_optimized.objects.all()
    T = []
    T_complete = []
    info = []
    info_complete = []
    for i in range(len(all_shippings)):
        if len(all_shippings[i].city_zwischenstopp):
            info_complete.append([all_shippings[i].city_sender, all_shippings[i].city_zwischenstopp, all_shippings[i].city_receiver])
        else:
            info.append(
                [all_shippings[i].city_sender, all_shippings[i].city_receiver])

    lat1, long1, lat2, long2 = float(41.40338), float(2.17403), float(46.592551), float(7.753058)
    route = getroute.get_route(long1, lat1, long2, lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])],
                   tooltip='This tooltip will appear on hover',
                   zoom_start=5)
    m.add_to(figure)
    counter = 0
    for i in range(len(all_shippings)):
        if all_shippings[i].longitude_zwischenstopp != 0:
            T_complete.append(
                [all_shippings[i].longitude_sender, all_shippings[i].latitude_sender, all_shippings[i].longitude_zwischenstopp,
                 all_shippings[i].latitude_zwischenstopp, all_shippings[i].longitude_receiver,all_shippings[i].latitude_receiver])
            for x in range(len(T_complete)):
                counter += 1
                route1 = getroute.get_route(T_complete[x][0], T_complete[x][1], T_complete[x][2], T_complete[x][3])
                route2 = getroute.get_route(T_complete[x][2], T_complete[x][3], T_complete[x][4], T_complete[x][5])
                if counter % 9 == 0:
                    folium.PolyLine(route1['route'], weight=8, color='black', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='black', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)

                elif counter % 9 == 1:
                    folium.PolyLine(route1['route'], weight=8, color='purple', opacity=0.4,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='purple', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 2:
                    folium.PolyLine(route1['route'], weight=8, color='darkgreen', opacity=0.4,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='darkgreen', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 3:
                    folium.PolyLine(route1['route'], weight=8, color='pink', opacity=0.6,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='pink', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 4:
                    folium.PolyLine(route1['route'], weight=8, color='red', opacity=0.4,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='red', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 5:
                    folium.PolyLine(route1['route'], weight=8, color='blue', opacity=0.4,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='blue', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 6:
                    folium.PolyLine(route1['route'], weight=8, color='gray', opacity=0.6,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='gray', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 7:
                    folium.PolyLine(route1['route'], weight=8, color='lightblue', opacity=0.8,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='lightblue', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                elif counter % 9 == 8:
                    folium.PolyLine(route1['route'], weight=8, color='darkred', opacity=0.4,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='darkred', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                else:
                    folium.PolyLine(route1['route'], weight=8, color='orange', opacity=0.7,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)
                    folium.PolyLine(route2['route'], weight=8, color='orange', opacity=0.5,
                                    popup=info_complete[x][0] + "-" + info_complete[x][1]).add_to(m)

                folium.Marker(location=route1['start_point'], opacity=0.7, clustered_marker=True,
                              icon=folium.Icon(icon='play', color='green', fill=True)).add_to(m)
                folium.Marker(location=route2['end_point'], opacity=0.7, clustered_marker=True,
                              icon=folium.Icon(icon='stop', color='red', fill=True)).add_to(m)
                folium.Marker(location=route1['end_point'], opacity=0.7, clustered_marker=True,
                              icon=folium.Icon(icon='stop', color='orange', fill=True)).add_to(m)

        else:
            T.append(
                [all_shippings[i].longitude_sender, all_shippings[i].latitude_sender,
                  all_shippings[i].longitude_receiver,all_shippings[i].latitude_receiver])
            for x in range(len(T)):
                counter += 1
                route1 = getroute.get_route(T[x][0], T[x][1], T[x][2], T[x][3])
                if counter % 9 == 0:
                    folium.PolyLine(route1['route'], weight=8, color='black', opacity=0.5,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)

                elif counter % 9 == 1:
                    folium.PolyLine(route1['route'], weight=8, color='purple', opacity=0.4,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 2:
                    folium.PolyLine(route1['route'], weight=8, color='darkgreen', opacity=0.4,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 3:
                    folium.PolyLine(route1['route'], weight=8, color='pink', opacity=0.6,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 4:
                    folium.PolyLine(route1['route'], weight=8, color='red', opacity=0.4,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 5:
                    folium.PolyLine(route1['route'], weight=8, color='blue', opacity=0.4,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 6:
                    folium.PolyLine(route1['route'], weight=8, color='gray', opacity=0.6,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 7:
                    folium.PolyLine(route1['route'], weight=8, color='lightblue', opacity=0.8,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                elif counter % 9 == 8:
                    folium.PolyLine(route1['route'], weight=8, color='darkred   ', opacity=0.4,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)
                else:
                    folium.PolyLine(route1['route'], weight=8, color='orange', opacity=0.7,
                                    popup=info[x][0] + "-" + info[x][1]).add_to(m)

                folium.Marker(location=route1['start_point'], opacity=0.7, clustered_marker=True,
                              icon=folium.Icon(icon='play', color='green', fill=True)).add_to(m)
                folium.Marker(location=route1['end_point'], opacity=0.7, clustered_marker=True,
                              icon=folium.Icon(icon='stop', color='red', fill=True)).add_to(m)





    figure.render()
    context = {'map': figure}
    return render(request,'accounts/routes_optimized.html',context)


def kpis(request):
    context = {}

    return render(request, 'accounts/kpis.html', context)

def chatbot(request):
    context = {}

    return render(request, 'accounts/chatbot.html', context)

def list(request):
    context = {}
    shipping_optimized.objects.filter(id=3435).update(address_receiver="Ścigały 20")
    context['medikamente'] = shipping_optimized.objects.all()
    context['past_shippings'] = ShippingInfo.objects.all()





    return render(request, 'accounts/list.html', context)


# konvertiert datatime data zu string
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


# patientenauswahl views, mit model patienteninfo
def patientenauswahl(request):
    context = {}
    context['medikamente'] = ShippingInfo.objects.all()
    return render(request, 'rezepterstellung/patientenauswahl.html', context)


def past_shippings(request):
    context = {}
    context['medikamente'] = ShippingInfo.objects.all()
    return render(request, 'rezepterstellung/medikamentauswahl.html', context)

def detailed_past_shippings(request):
    context = {}
    system = request.POST.get('system', None)
    if system is not None:
        if "," in system:
            x = system.split(",")
            print(x)
            desired_array = [int(numeric_string) for numeric_string in x]
            y = ShippingInfo.objects.filter(id=desired_array[0])
            z = ShippingInfo.objects.filter(id=desired_array[1] )
            context['medikamente'] = y | z

        else:
            context['medikamente'] = ShippingInfo.objects.filter(id=int(system))
    return render(request, 'accounts/detailed_past_shippings.html', context)





# ladet login page, falls request post ist, wird kontrolliert ob der user
# existiert, falls ja wird er eingeloggt.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('arzt-home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            praxis = authenticate_praxis(request, email=email, password=password)
            admin = authenticate_admin(request, email=email, password=password)

            try:
                user_to_authenticate_acc = CustomUser.objects.get(email=email).accepted_by_praxis
                user_type = CustomUser.objects.get(email=email).fachrichtung
                if user_to_authenticate_acc==True:
                    user = authenticate(request, email=email, password=password)
                elif user_to_authenticate_acc==False and user_type == "Richtung auswählen":
                    user = "not accepted by apotheke"
                elif user_to_authenticate_acc==False and user_type != 'Richtung auswählen':
                    user = "not accepted by praxis"
                else:
                    user = None
            except CustomUser.DoesNotExist:
                user = None
            if praxis is not None and praxis != "not yet validated":
                login(request,praxis,backend='accounts.backends.MyBackend')
                return redirect('praxis-home')
            if admin is not None:
                login(request, admin, backend='accounts.backends.AdminBackend')
                return redirect('/admin-page')
            if user is not None and user != "not accepted by praxis" and user != "not accepted by apotheke":
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('arzt-home')
            if praxis is None and user is None:
                messages.info(request, 'Email oder Passwort ist falsch')
            if praxis=="not yet validated":
                messages.info(request, 'Sie wurden noch nicht von Medorg akzeptiert')
            if user=="not accepted by praxis":
                messages.info(request, 'Sie wurden noch nicht von Ihrer Praxis angenommen')
            if user=="not accepted by apotheke":
                messages.info(request, 'Sie wurden noch nicht von Ihrer Apotheke angenommen')

        context = {}
        return render(request, 'accounts/login.html', context)

def signout(request):
    logout(request)
    return redirect('login')


def admin_page(request):
    context = {}
    praxen = Praxis.objects.all()
    context['praxen'] = praxen


    return render(request, 'accounts/admin_page.html', context)




# ladet startseite eines arztes nach login.
@login_required(login_url="login")
@arzt_only
def home(request):
    context = {}
    arzt_id = CustomUser.objects.get(id=request.user.id)


    context.update({
        'arzt_id': arzt_id,

    })
    return render(request, 'accounts/home.html', context)


# funkion zum ausloggen eines users
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
@praxis_only
def praxis_home(request):
    form = ShippingInfoForm()
    context = {}
    system = request.GET.get('system', None)
    if system is not None:
        copied_shipment = ShippingInfo.objects.get(id=system)
        context['copied_shipment'] = copied_shipment
    else:
        context['copied_shipment'] = 0
    if request.method == 'POST':
        form = ShippingInfoForm(request.POST)
        if form.is_valid():
            shipping_info = form.save(commit=False)
            shipping_info.save()

            return redirect('/medikamentauswahl/')
        else:
            print(form.errors.as_data())

    context['form'] = form
    return render(request, 'accounts/praxis-home.html', context)


