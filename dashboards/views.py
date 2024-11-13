# Django
import re
from django.db.models import Q, Max, Subquery, Count, F, Func, ExpressionWrapper, DurationField, IntegerField, DateTimeField, Min, OuterRef, Case, When, Value
from django.db.models.functions import Coalesce, ExtractDay, TruncDate, Now, Extract, Cast
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, DeleteView, UpdateView
from django.views.generic.base import View

# Functions
from dashboards import functions
from crm import settings

# Forms
from dashboards.forms import LeadForm

# Models
from django.contrib.auth.models import User, Group
from dashboards.models import Prospecto, Asesor, Catalogo, CatalogoModelo, Lead, CatalogoRespuestasByEtapa, Historial, HistorialVerificaciones, Retomas, VehiculosInteresLead, Evento

# Utilities
import ast
import csv
from datetime import date, datetime, timedelta
import json
import pandas as pd
import xlwt

class DateDiff(Func):
    function = 'DATEDIFF'
    output_field = IntegerField()

class DiffDays(Func):
    function = 'DATE_PART'
    template = "%(function)s('day', %(expressions)s)"

class CastDate(Func):
    function = 'date_trunc'
    template = "%(function)s('day', %(expressions)s)"

class LoginView(auth_views.LoginView):
    # Vista de Login

    template_name = "Login.html"
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    # Vista de Logout
    pass

class CapturaView(LoginRequiredMixin, TemplateView):
    # Vista de Captura

    template_name = "Captura.html"

    def get_context_data(self, **kwargs):

        # df = pd.read_excel(r'c:\Users\cndesarrollo\Documents\CATALOGO DE VEHICULOS Y ORIGEN LEAD.xlsx', sheet_name='CATALOGO DE VEHICULOS', header=2)

        # data_dict = {}

        # print("Nombres de columnas:", df.columns.tolist())

        # for columna in df.columns:
        #     data_dict[columna] = df[columna].tolist()

        # marca_actual = None

        # for i in range(156):

        #     if type(data_dict["Marcas de vehiculos"][i]) != float:
        #         marca_actual = data_dict["Marcas de vehiculos"][i]

        #     print(f'Marca: {marca_actual}. Modelo: {data_dict["Modelos de vehiculos"][i]}')

        #     if type(data_dict["Modelos de vehiculos"][i]) != float:

        #         first_year = int(data_dict["año"][i].split("-")[0])
        #         last_year = int(data_dict["año"][i].split("-")[1])

        #         years_list = [str(anio) for anio in range(first_year, last_year + 1)]
        #         print(years_list)



        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        nombre = user.first_name

        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        now = datetime.now()
        
        leads = Lead.objects.all()
        prospectos = Prospecto.objects.all()
        historiales = Historial.objects.all()
        vehiculos = VehiculosInteresLead.objects.all()
        verificaciones = HistorialVerificaciones.objects.all()

        """for verificacion in verificaciones:
            verificacion.tipo = "venta"
            verificacion.save()
            print(verificacion)"""

        lista_historial = []

        """for v in vehiculos:
            print(v)
            if v.cotizar:
                v.mostrado = True
                v.save()"""


        """for historial in historiales:
            if historial.lead.id in lista_historial:
                pass
            else:
                if historial.operacion[0:31] == "El cliente a dado una respuesta":
                    lead = Lead.objects.get(id=historial.lead.id)
                    fecha_completa = datetime.strptime(str(historial.fecha) + " " + str(historial.hora), '%Y-%m-%d %H:%M:%S')
                    lead.fecha_primer_contacto = fecha_completa
                    print(fecha_completa)

                    try:
                        lead.tiempo_primer_contacto = (fecha_completa.replace(tzinfo=None) - lead.fecha_hora_asignacion_asesor.replace(tzinfo=None)).total_seconds() / 60
                        lead.save()
                        lista_historial.append(lead.id)
                        print(lead.id)
                    except:
                        pass"""

        """for lead in leads:
            lead.tiempo_cambio_de_etapa = None
            print(lead)
            lead.save()"""

        """for lead in leads:
            fecha_apertura = lead.fecha_apertura
            fecha = datetime(fecha_apertura.year, fecha_apertura.month, fecha_apertura.day)
            lead.fecha_apertura = fecha
            print(lead)
            lead.save()"""
            

        """for row in sheet.iter_rows(min_row=2):
            username = row[6].value
            activo = row[8].value
            if activo == "Inactivo" or activo == "AsesorInactivo":
                activo = False
            else:
                activo = True
            if username != "null" and username != "NULL" and username != "":
                user = User.objects.get(username=username)
                user.is_active = activo
                user.save()"""

        """for row in sheet.iter_rows(min_row=2):
            name = row[1].value
            group = row[3].value
            correo = row[5].value
            username = row[6].value
            password = row[7].value
            if username != "null" and username != "NULL" and username != "":
                user = User.objects.create(username=username, 
                                        password=password,
                                        first_name=name,
                                        email=correo)
                if_grupo = True
                if group == "AdminCompras":
                    group = "Admin Compras"
                elif group == "Anfitrion":
                    group = "Anfitrión"
                elif group == "Anfitrion/PefiladoraInactivo":
                    group = "Anfitrión"
                elif group == "AnfitrionInactivo":
                    group = "Anfitrión"
                elif group == "AsesorInactivo":
                    group = "Asesor"
                elif group == "CompradorInactivo":
                    group = "Comprador"
                elif group == "Jefe de Sala":
                    group = "Jefe de sala"
                elif group == "PeritoInactivo":
                    group = "Perito"
                elif group == "Lider CRM":
                    if_grupo = False
                
                if if_grupo:
                    grupo = Group.objects.get(name=group)
                    user.groups.add(grupo)"""

        """for prospecto in prospectos:
            if len(prospecto.correo) < 4:
                prospecto.correo = ""
                print("prospecto")
                print(prospecto.id)
                prospecto.save()"""

        calendario_general = True
        origenes_lead = Catalogo.objects.filter(clasificacion="Origen Lead")

        asesores = Asesor.objects.all()
        grupo = Group.objects.get(name="Asesor")

        marcas = CatalogoModelo.objects.all().values("marca").distinct()

        
        cantidad_ecatepec = Lead.objects.filter(sala="Xalostoc Ecatepec", fecha_apertura__month=now.month, fecha_apertura__year=now.year).count()

        today = datetime.now()

        anfitrion_group = Group.objects.get(name="Anfitrion")
        anfitriones = User.objects.filter(groups=anfitrion_group, is_active=True)

        context["anfitriones"] = anfitriones
        context["asesor_actual"] = asesor_actual
        context["calendario_general"] = calendario_general
        context["cantidad_ecatepec"] = cantidad_ecatepec
        context["marcas"] = marcas
        context["nombre"] = nombre
        context["today"] = today
        context["origenes_lead"] = origenes_lead
        context["user"] = user

        
        return context

    def post(self, request):
        r = request.POST
        user = User.objects.get(username=self.request.user)
        
        print(r)
        if r.get("celular_verificar", None):
            prospecto = Prospecto.objects.get(celular=r.get("celular_verificar", None))
            print(prospecto)
            if prospecto:
                ultimo_lead = Lead.objects.filter(prospecto=prospecto).last()
                ultimo_lead = {"nombre_anfitrion": ultimo_lead.nombre_anfitrion, "fecha_apertura": ultimo_lead.fecha_apertura.date(), "respuesta": ultimo_lead.respuesta, "estado": ultimo_lead.estado, "nombre_asesor": ultimo_lead.nombre_asesor,}
                alerta = {"alerta_celular": True, "ultimo_lead": ultimo_lead}
            else:
                alerta = {"alerta_celular": False}

            return JsonResponse(alerta, safe=False)
        
        if r.get("marca", None):
            marca = r.get("marca", None)
            modelos = CatalogoModelo.objects.filter(marca=marca.title())
            print(marca.title())
            print("modelos")
            print(modelos)
            modelos = list(modelos.values())

            print(modelos)

            return JsonResponse(modelos, safe=False)
        if r.get("InfoProspecto", None):
            celular = r.get("Celular", None)
            prospecto = Prospecto.objects.get(celular=celular)
            prospecto = [prospecto.nombre, prospecto.apellido_paterno, prospecto.apellido_materno, prospecto.correo]

            return JsonResponse(prospecto, safe=False)
        if r.get("NombreProspecto", None):
            nombre = r.get("NombreProspecto", None)
            apellido_paterno = r.get("ApellidoPProspecto", None)
            apellido_materno = r.get("ApellidoMProspecto", None)
            celular = r.get("Celular", None)
            correo = r.get("Correo", None)
            origen_lead = r.get("OrigenLead", None)
            campania = r.get("Campania", None)
            tipo_documento = r.get("TipoDocumento", None)
            documento = r.get("Documento", None)
            politica_privacidad = r.get("PoliticaPrivacidad", None)
            if not politica_privacidad:
                politica_privacidad = False
            else:
                politica_privacidad = True
            anfitrion = r.get("Anfitrion", None)
            sala = r.get("Sala", None)
            nombre_asesor = r.get("Asesor", None)
            marcas_interes = r.getlist("MarcasInteres[]", None)
            marca = json.loads(r.get("Marca", None))
            placa = json.loads(r.get("Placa", None))
            modelo = json.loads(r.get("Modelo", None))
            cilindros = json.loads(r.get("Cilindros", None))
            tipo_inyeccion = json.loads(r.get("TipoInyeccion", None))
            print(marcas_interes)
            print(marca)
            print(placa)
            print(modelo)
            print(cilindros)
            print(tipo_inyeccion)
            if not(nombre_asesor) or nombre_asesor == "":
                pass
            else:
                m_lista = []
                for ma in range(len(marcas_interes)):
                    try:
                        if len(modelo[ma]) != 0:
                            for mo in range(len(modelo[ma])):
                                print("aver la marca de interees")
                                print(marcas_interes[ma])
                                print(placa[ma][mo])
                                print(modelo[ma][mo])
                                print(cilindros[ma][mo])
                                print(tipo_inyeccion[ma][mo])
                                if marcas_interes[ma] == "OTROS":
                                    marca_real = marca[mo]
                                else:
                                    marca_real = marcas_interes[ma]
                                m_lista.append({"marca": marca_real,
                                    "placa": placa[ma][mo],
                                    "vin": "",
                                    "tipo_tanque": "",
                                    "modelo": modelo[ma][mo],
                                    "cilindros": cilindros[ma][mo],
                                    "marca_comentario": None,
                                    "tipo_inyeccion": tipo_inyeccion[ma][mo],
                                    "kit_conversion": "",
                                    })
                        else:
                            m_lista.append({"marca": marcas_interes[ma],
                                "placa": "",
                                "vin": "",
                                "tipo_tanque": "",
                                "modelo": "",
                                "cilindros": "",
                                "marca_comentario": None,
                                "tipo_inyeccion": "",
                                "kit_conversion": "",
                                })
                    except:
                        m_lista.append({"marca": marcas_interes[ma],
                                "placa": "",
                                "vin": "",
                                "tipo_tanque": "",
                                "modelo": "",
                                "cilindros": "",
                                "marca_comentario": None,
                                "tipo_inyeccion": "",
                                "kit_conversion": "",
                                })
                    
                marcas = {"marcas": m_lista}
                comentario = r.get("Comentario", None)
                test_drive = r.get("TestDrive", None)
                if not test_drive:
                    test_drive = False
                else:
                    test_drive = True
            
            print("marcas")
            print(marcas)

            try:
                prospecto = Prospecto.objects.get(celular=celular)
                prospecto.nombre=nombre
                prospecto.apellido_paterno=apellido_paterno
                prospecto.apellido_materno=apellido_materno
                prospecto.correo=correo
                prospecto.save()
            except:
                prospecto = Prospecto.objects.create(nombre=nombre,
                                apellido_paterno=apellido_paterno,
                                apellido_materno=apellido_materno,
                                celular=celular,
                                correo=correo,
                                fecha_captura=make_aware(datetime.now()),
                                nombre_asesor=nombre_asesor,
                                anfitrion=anfitrion,
                                fecha_hora_asignacion_asesor=make_aware(datetime.now()),
                                politica_privacidad=politica_privacidad,
                                )
            
            lead = Lead.objects.create(prospecto=prospecto,
                                origen_lead=origen_lead,
                                marcas_interes=marcas,
                                sala=sala,
                                etapa="No contactado",
                                respuesta="Sin contactar",
                                estado="No contactado",
                                status="Frío",
                                interes="Venta",
                                activo=True,
                                fecha_apertura=make_aware(datetime.now()),
                                comentario=comentario,
                                campania=campania,
                                tipo_documento=tipo_documento,
                                documento=documento,
                                test_drive=test_drive,
                                nombre_asesor=nombre_asesor,
                                nombre_asesor_original=nombre_asesor,
                                fecha_hora_asignacion_asesor=make_aware(datetime.now()),
                                nombre_anfitrion=anfitrion,
                                )
            Historial.objects.create(lead=lead,
                        fecha=date.today(),
                        hora=datetime.now().time(),
                        responsable=user,
                        operacion=f"Creación Lead",
                        comentarios=comentario
                        )
            if marcas_interes:
                try:
                    mod = modelo[0][0]
                except:
                    mod = ""
                try:
                    cil = cilindros[0][0]
                except:
                    cil = ""
                VehiculosInteresLead.objects.create(lead=lead,
                                                marca=marcas_interes[0],
                                                modelo=mod,
                                                cilindros=cil,
                                                peritaje=False,
                                                cotizar=False,
                                                aprobacion=False,
                                                precio=None,
                                                separado=False,
                                                facturado=False,
                                                mostrado=True,
                                                fecha=date.today(),
                                                )
            return HttpResponse(reverse_lazy('dashboards:captura'))

        if r.get("sala", None):
            sala = r.get("sala", None)
            asesores = Asesor.objects.filter(Q(habilitado=True) | Q(habilitado=None), sala=sala)
            print("asesores")
            print(asesores)
            asesores = list(asesores.values())

            return JsonResponse(asesores, safe=False)

        if r.get("etapa", None):
            etapa = r.get("etapa", None)
            respuestas = CatalogoRespuestasByEtapa.objects.filter(etapa=etapa).values("respuesta").distinct()
            print("respuestas")
            print(respuestas)
            respuestas = list(respuestas)

            return JsonResponse(respuestas, safe=False)

        

class CapturaReasignamientoView(LoginRequiredMixin, DetailView):
    # Vista de Captura Reasignamiento

    template_name = "CapturaReasignamiento.html"
    slug_field = "lead"
    slug_url_kwarg = "lead"
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        asesores = Asesor.objects.all()
        grupo = Group.objects.get(name="Asesor")

        marcas = CatalogoModelo.objects.all().values("marca").distinct()

        now = datetime.now()

        cantidad_ecatepec = Lead.objects.filter(sala="Xalostoc Ecatepec", fecha_apertura__month=now.month).count()

        today = datetime.now()

        calendario_general = True
        origenes_lead = Catalogo.objects.filter(clasificacion="Origen Lead")
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False
                origenes_lead = Catalogo.objects.filter(clasificacion="Origen Lead Asesor")

        context["asesor_actual"] = asesor_actual
        context["calendario_general"] = calendario_general
        context["cantidad_ecatepec"] = cantidad_ecatepec
        context["origenes_lead"] = origenes_lead
        context["marcas"] = marcas
        context["today"] = today
        context["user"] = user
        return context
    
    def post(self, request, pk):
        r = request.POST
        user = User.objects.get(username=self.request.user)
        

        if r.get("sala", None):
            sala = r.get("sala", None)
            asesores = Asesor.objects.filter(sala=sala)
            print("asesores")
            print(asesores)
            asesores = list(asesores.values())

            return JsonResponse(asesores, safe=False)

        if r.get("Asesor", None):
            sala = r.get("Sala", None)
            nombre_asesor = r.get("Asesor", None)

            lead = Lead.objects.get(pk=pk)
            lead.sala = sala
            lead.nombre_asesor = nombre_asesor
            lead.fecha_hora_asignacion_asesor = datetime.now()
            lead.fecha_hora_reasignacion = datetime.now()
            lead.tiempo_primer_contacto = None
            lead.fecha_primer_contacto = None
            lead.etapa = "No contactado"
            lead.respuesta = "Sin contactar"
            lead.estado = "No contactado"
            lead.save()
            
            Historial.objects.create(lead=lead,
                        fecha=date.today(),
                        hora=datetime.now().time(),
                        responsable=user,
                        operacion=f"Reasignación de asesor a {nombre_asesor}",
                        comentarios=None
                        )
            return HttpResponseRedirect(reverse_lazy('dashboards:captura'))


class DetalleClienteView(LoginRequiredMixin, TemplateView):
    # Vista de Detalle Cliente

    template_name = "DetalleCliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        context["asesor_actual"] = asesor_actual
        context["calendario_general"] = calendario_general
        context["user"] = user

        return context

class DetalleClienteNuevoView(LoginRequiredMixin, DetailView):
    # Vista de Detalle Cliente Nuevo

    template_name = "DetalleClienteNuevo.html"
    slug_field = "lead"
    slug_url_kwarg = "lead"
    queryset = Lead.objects.all()
    context_object_name = "lead"
    form_class = LeadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()

        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        historial = Historial.objects.filter(lead=lead)

        prospecto = Prospecto.objects.get(pk=lead.prospecto.pk)
        try:
            sala = Asesor.objects.get(nombre=lead.nombre_asesor).sala
        except:
            sala = None

        asesor_group = Group.objects.get(name="Asesor")
        asesores_user = list(User.objects.filter(groups=asesor_group, is_active=True).values_list("first_name", flat=True))
        asesores = Asesor.objects.filter(sala=sala, nombre__in=asesores_user)

        if lead.fecha_hora_asignacion_asesor:

            dias_totales = (make_aware(datetime.now()) - lead.fecha_hora_asignacion_asesor).days

            tiempo_diferencia = int((make_aware(datetime.now()) - lead.fecha_hora_asignacion_asesor).total_seconds() / 60)
        
            # print(make_aware(datetime.now()))
            # print(lead.fecha_hora_asignacion_asesor)
            # print((make_aware(datetime.now()) - lead.fecha_hora_asignacion_asesor).total_seconds())
            # print(tiempo_diferencia)
            # print(lead.tiempo_primer_contacto)

            if lead.tiempo_primer_contacto or tiempo_diferencia:
                functions.verificar_primer_contacto(lead, prospecto, tiempo_diferencia)

        else:
            dias_totales = 0
            tiempo_diferencia = 0

        modelos = ""
        if lead.marcas_interes:
        
            marcas_interes = eval(lead.marcas_interes)
            for marca in marcas_interes["marcas"]:
                modelos = CatalogoModelo.objects.filter(marca=marca["marca"])

                modelos = list(modelos.values_list("nombre", flat=True))

        else:
            marcas_interes = ""
        marcas = CatalogoModelo.objects.all().values("marca").distinct()

        subquery = CatalogoRespuestasByEtapa.objects.filter(etapa=OuterRef("etapa")).order_by("id").values("id")[:1]

        etapas = (CatalogoRespuestasByEtapa.objects.filter(id__in=Subquery(subquery)).annotate(
                    custom_order=Case(
                    When(etapa="Desistido", then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', 'etapa'))

        respuestas = CatalogoRespuestasByEtapa.objects.filter(etapa=lead.etapa).values("respuesta").distinct()

        mostrar_evento = False
        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                mostrar_evento = True
                calendario_general = False
            if grupo.name == "Admin":
                mostrar_evento = True

        context["asesor_actual"] = asesor_actual
        context["asesores"] = asesores
        context["calendario_general"] = calendario_general
        context["dias_totales"] = dias_totales
        context["etapas"] = etapas
        context["historial"] = historial
        context["marcas"] = marcas
        context["marcas_interes"] = marcas_interes
        context["modelos"] = modelos
        context["mostrar_evento"] = mostrar_evento
        context["prospecto"] = prospecto
        context["respuestas"] = respuestas
        context["sala"] = sala
        context["tiempo_diferencia"] = tiempo_diferencia
        context["user"] = user



        # Cadena original
        # leads = Lead.objects.filter(nombre_asesor="Gustavo Parraga")
        # for lead in leads:
        #     historial_f = Historial.objects.filter(lead=lead, operacion__startswith="Se modificaron los siguientes campos: ['Etapa.")
        #     if historial_f.exists():
        #         cadena = historial_f.last().operacion

        #         # Expresión regular para capturar los campos y sus valores actuales
        #         pattern = r"(\w+)\.\s*\(.*?Ahora:\s*(.*?)\)"

        #         # Buscar coincidencias en la cadena
        #         matches = re.findall(pattern, cadena)

        #         # Construir el diccionario a partir de las coincidencias
        #         resultado = {campo: valor.strip() for campo, valor in matches}

        #         # Imprimir el resultado
        #         lead.etapa = resultado["Etapa"]
        #         lead.estado = resultado["Etapa"]
        #         lead.respuesta = resultado["Respuesta"]
        #         lead.save()
        #         print("resultado")
        #         print(resultado)

        return context
    
    def post(self, request, pk):

        print(request.POST)
        lead = Lead.objects.get(pk=pk)
        prospecto = Prospecto.objects.get(pk=lead.prospecto.pk)
        user = User.objects.get(username=self.request.user)
        if request.POST.get("Lead_Etapa"):
            lista_historial = []
            if lead.etapa != request.POST.get("Lead_Etapa"):
                lista_historial.append(f"Etapa. (Antes: {lead.etapa}. Ahora: {request.POST.get('Lead_Etapa')})")
            lead.etapa = request.POST.get("Lead_Etapa")
            lead.estado = request.POST.get("Lead_Etapa")
            if lead.respuesta != request.POST.get("Lead_Respuesta"):
                lista_historial.append(f"Respuesta. (Antes: {lead.respuesta}. Ahora: {request.POST.get('Lead_Respuesta')})")
            lead.respuesta = request.POST.get("Lead_Respuesta")
            comentario = request.POST.get("Lead_Comentario")
            if lead.comentario != comentario and comentario != "None":
                lista_historial.append(f"Comentario. (Antes: {lead.comentario}. Ahora: {request.POST.get('Lead_Comentario')})")
            lead.comentario = request.POST.get("Lead_Comentario")
            if request.POST.get("Lead_Respuesta") != "Sin contactar":
                if not(lead.fecha_primer_contacto):
                    lead.fecha_primer_contacto = datetime.now()
                    try:
                        tiempo_primer_contacto = datetime.now() - lead.fecha_hora_asignacion_asesor.replace(tzinfo=None)
                    except:
                        tiempo_primer_contacto = datetime.now() - lead.fecha_hora_reasignacion.replace(tzinfo=None)
                    lead.tiempo_primer_contacto = tiempo_primer_contacto.total_seconds() / 60
                else:
                    lead.fecha_cambio_de_etapa = datetime.now()
                    tiempo_cambio_de_etapa = datetime.now() - lead.fecha_primer_contacto.replace(tzinfo=None)
                    lead.tiempo_cambio_de_etapa = tiempo_cambio_de_etapa.total_seconds() / 60

            marcas_interes = request.POST.getlist("MarcasInteres[]", None)
            marca = json.loads(request.POST.get("Marca", None))
            placa = json.loads(request.POST.get("Placa", None))
            vin = json.loads(request.POST.get("Vin", None))
            tipo_tanque = json.loads(request.POST.get("TipoTanque", None))
            modelo = json.loads(request.POST.get("Modelo", None))
            cilindros = json.loads(request.POST.get("Cilindros", None))
            tipo_inyeccion = json.loads(request.POST.get("TipoInyeccion", None))
            kit_conversion = json.loads(request.POST.get("KitConversion", None))
            
            codigo_vehiculo = request.POST.getlist("CodigoVehiculo", None)

            lista_marcas_interes = request.POST.getlist("ListaMarcasInteres[]", None)
            lista_placas = request.POST.getlist("ListaPlacas[]", None)
            lista_vin = request.POST.getlist("ListaVin[]", None)
            lista_tipo_tanque = request.POST.getlist("ListaTipoTanque[]", None)
            lista_modelos = request.POST.getlist("ListaModelos[]", None)
            lista_cilindros = request.POST.getlist("ListaCilindros[]", None)
            lista_tipo_inyeccion = request.POST.getlist("ListaTipoInyeccion[]", None)
            lista_kit_conversion = request.POST.getlist("ListaKitConversion[]", None)

            marcas_lista = eval(lead.marcas_interes)["marcas"]
            m_lista = []

            print("marcas_interes")
            print(marcas_interes)
            print("marca")
            print(marca)
            print("placa")
            print(placa)
            print("lista_placas")
            print(lista_placas)
            print("lista_vin")
            print(lista_vin)
            print("lista_tipo_tanque")
            print(lista_tipo_tanque)
            print("lista_modelos")
            print(lista_modelos)
            print("lista_cilindros")
            print(lista_cilindros)

            for ma in range(len(lista_marcas_interes)):
                m_lista.append({"marca": lista_marcas_interes[ma],
                    "placa": lista_placas[ma],
                    "vin": lista_vin[ma],
                    "tipo_tanque": lista_tipo_tanque[ma],
                    "modelo": lista_modelos[ma],
                    "cilindros": lista_cilindros[ma],
                    "marca_comentario": None,
                    "tipo_inyeccion": lista_tipo_inyeccion[ma],
                    "kit_conversion": lista_kit_conversion[ma],
                    })

            if len(marcas_lista) == 0:
                try:
                    VehiculosInteresLead.objects.create(lead=lead,
                                                marca=marcas_interes[0],
                                                modelo=modelo[0][0],
                                                cilindros=cilindros[0][0],
                                                tipo_inyeccion=tipo_inyeccion[0][0],
                                                kit_conversion=kit_conversion[0][0],
                                                peritaje=False,
                                                cotizar=False,
                                                aprobacion=False,
                                                separado=False,
                                                facturado=False,
                                                mostrado=True,
                                                fecha=date.today(),
                                                )
                except:
                    pass


            print(modelo)

            for ma in range(len(marcas_interes)):
                print("ma")
                print(ma)
                if modelo:
                    for mo in range(len(modelo[ma])):
                        print("mo")
                        print(mo)
                        print(marcas_interes[ma])
                        print(placa[ma][mo])
                        print(vin[ma][mo])
                        print(modelo[ma][mo])
                        if marcas_interes[ma] == "OTROS":
                            marca_real = marca[mo]
                        else:
                            marca_real = marcas_interes[ma]
                        try:
                            pla = placa[ma][mo]
                        except:
                            pla = ""
                        try:
                            vi = vin[ma][mo]
                        except:
                            vi = ""
                        try:
                            tip = tipo_tanque[ma][mo]
                        except:
                            tip = ""
                        try:
                            cil = cilindros[ma][mo]
                        except:
                            cil = ""
                        try:
                            iny = tipo_inyeccion[ma][mo]
                        except:
                            iny = ""
                        try:
                            kit = kit_conversion[ma][mo]
                        except:
                            kit = ""
                        m_lista.append({"marca": marca_real,
                            "placa": pla,
                            "vin": vi,
                            "tipo_tanque": tip[ma][mo],
                            "modelo": modelo[ma][mo],
                            "cilindros": cil,
                            "marca_comentario": None,
                            "tipo_inyeccion": iny,
                            "kit_conversion": kit,
                            })
                else:
                    m_lista.append({"marca": marcas_interes[ma],
                        "placa": "",
                        "vin": "",
                        "tipo_tanque": "",
                        "modelo": "",
                        "cilindros": "",
                        "marca_comentario": None,
                        "tipo_inyeccion": "",
                        "kit_conversion": "",
                        })
                
            marcas = {"marcas": m_lista}

            print(lead.marcas_interes)
            print(marcas)

            if str(lead.marcas_interes) != str(marcas):
                lista_historial.append(f"Marcas Interes. (Se agregaron: {m_lista})")
            lead.marcas_interes = marcas
            lead.save()
            
            if lista_historial:
                Historial.objects.create(lead=lead,
                                        fecha=date.today(),
                                        hora=datetime.now().time(),
                                        responsable=user,
                                        operacion=f"Se modificaron los siguientes campos: {lista_historial}",
                                        comentarios=comentario
                                        )
            return redirect("dashboards:detallenuevo", pk)
        elif request.POST.get("ProspectoNombre"):
            lista_historial = []
            if prospecto.nombre != request.POST.get("ProspectoNombre"):
                lista_historial.append("Nombre")
            prospecto.nombre = request.POST.get("ProspectoNombre")
            if prospecto.apellido_paterno != request.POST.get("ProspectoApPaterno"):
                lista_historial.append("Apellido Paterno")
            prospecto.apellido_paterno = request.POST.get("ProspectoApPaterno")
            if prospecto.apellido_materno != request.POST.get("ProspectoApMaterno"):
                lista_historial.append("Apellido Materno")
            prospecto.apellido_materno = request.POST.get("ProspectoApMaterno")
            if prospecto.celular != request.POST.get("ProspectoCelular"):
                lista_historial.append("Celular")
            prospecto.celular = request.POST.get("ProspectoCelular")
            if prospecto.correo != request.POST.get("ProspectoCorreo"):
                lista_historial.append("Correo")
            prospecto.correo = request.POST.get("ProspectoCorreo")
            prospecto.anfitrion = request.POST.get("Lead_NombreAnfitrion")
            if prospecto.contacto_nombre != request.POST.get("NombreContacto"):
                lista_historial.append("Nombre Contacto")
            prospecto.contacto_nombre = request.POST.get("NombreContacto")
            if prospecto.contacto_telefono != request.POST.get("CelularContacto"):
                lista_historial.append("Celular Contacto")
            prospecto.contacto_telefono = request.POST.get("CelularContacto")
            if request.POST.get("PoliticaDatos") == "true":
                politica_privacidad = True
            else:
                politica_privacidad = False
            if prospecto.politica_privacidad != politica_privacidad:
                lista_historial.append("Politica Datos")
            prospecto.politica_privacidad = politica_privacidad
            prospecto.save()

            if lead.nombre_anfitrion != request.POST.get("Lead_NombreAnfitrion"):
                lista_historial.append("Anfitrión")
            lead.nombre_anfitrion = request.POST.get("Lead_NombreAnfitrion")
            if lead.campania != request.POST.get("LeadCampania"):
                lista_historial.append("Campaña")
            lead.campania = request.POST.get("LeadCampania")
            if lead.tipo_documento != request.POST.get("LeadTipoDocumento"):
                lista_historial.append("Tipo de documento")
            lead.tipo_documento = request.POST.get("LeadTipoDocumento")
            if lead.documento != request.POST.get("LeadDocumento"):
                lista_historial.append("Documento")
            lead.documento = request.POST.get("LeadDocumento")
            if request.POST.get("TestDrive") == "true":
                test_drive = True
            else:
                test_drive = False
            if lead.test_drive != test_drive:
                lista_historial.append("TestDrive")
            lead.test_drive = test_drive
            lead.save()
            if lista_historial:
                Historial.objects.create(lead=lead,
                                        fecha=date.today(),
                                        hora=datetime.now().time(),
                                        responsable=user,
                                        operacion=f"Se modificaron los siguientes campos: {lista_historial}"
                                        )
            return JsonResponse(prospecto.pk, safe=False)
        elif request.POST.get("EstadoLlamada"):
            lista_historial = []

            estado_llamada = request.POST.get("EstadoLlamada")
            tipo_solicitud = request.POST.get("TipoSolicitud")
            reasignado = request.POST.get("AsesorReasignado")
            observaciones = request.POST.get("Observaciones")
            
            if reasignado:
                lead.nombre_asesor = reasignado
                lead.tiempo_primer_contacto = None
                lead.fecha_primer_contacto = None
                lead.fecha_hora_asignacion_asesor = None
                lead.fecha_hora_reasignacion = datetime.now()
            lead.estado_llamada_verificacion = estado_llamada
            lead.tipo_solicitud_verificacion = tipo_solicitud
            lead.save()

            HistorialVerificaciones.objects.create(lead=lead,
                                                   estado_llamada=estado_llamada,
                                                   tipo_solicitud=tipo_solicitud,
                                                   responsable=user,
                                                   reasignado=reasignado,
                                                   observaciones=observaciones,
                                                   fecha_hora_verificacion=datetime.now(),
                                                   tipo="venta"
                                                   )
            if not(reasignado):
                reasignado = ""
            else:
                reasignado = f"Reasignado a: {reasignado}"


            Historial.objects.create(lead=lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se hizo la verificación. Estado de llamada: {estado_llamada}. Tipo de solicitud: {tipo_solicitud}. {reasignado}",
                                    comentarios=observaciones
                                    )
            return JsonResponse(prospecto.pk, safe=False)
        elif request.POST.get("vehiculo_cita[]"):
            lista_historial = []

            vehiculo_cita = request.POST.get("vehiculo_cita[]")
            deposito_apartado = request.POST.get("deposito_apartado[]")
            precio_conversion = request.POST.get("precio_conversion[]")
            fecha_programacion = request.POST.get("fecha_programacion[]")
            forma_pago = request.POST.get("forma_pago[]")

            print(vehiculo_cita)
            print(deposito_apartado)
            print(precio_conversion)
            print(fecha_programacion)
            print(forma_pago)

            Historial.objects.create(lead=lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se agendó la cita. Vehículo: {vehiculo_cita}. Depósito apartado: {deposito_apartado}. Precio conversión: {precio_conversion}. Fecha programación: {fecha_programacion}. Forma pago: {forma_pago}.",
                                    )
            return JsonResponse(prospecto.pk, safe=False)
        elif request.POST.get("deposito_apartado"):
            cita_vehiculo = request.POST.get("cita_vehiculo")
            deposito_apartado = request.POST.get("deposito_apartado")
            precio_conversion = request.POST.get("precio_conversion")
            fecha_programacion = request.POST.get("fecha_programacion")
            forma_pago = request.POST.get("forma_pago")

            Historial.objects.create(
                lead=lead,
                fecha=date.today(),
                hora=datetime.now().time(),
                responsable=user,
                operacion=f"{deposito_apartado} se apartó el depósito. Precio de conversión: {precio_conversion}. Modelo: {cita_vehiculo}. Fecha de programación: {fecha_programacion}. Forma de pago: {forma_pago}.",
            )
            return JsonResponse(prospecto.pk, safe=False)
        elif request.POST.get("EventoNombre"):

            nombre = request.POST.get("EventoNombre")
            tipo = request.POST.get("EventoTipo")
            telefono_cliente = request.POST.get("EventoTelefono")
            observaciones = request.POST.get("EventoObservaciones")
            asesor = request.POST.get("EventoAsesor")
            fecha_hora = request.POST.get("EventoFechaHora")
            tiempo_evento = request.POST.get("EventoTiempo")

            print("fecha_hora")
            print(type(fecha_hora))

            print(date.today())
            print(type(date.today()))

            print(datetime.now().time())
            print(type(datetime.now().time()))

            prospecto = Prospecto.objects.get(celular=telefono_cliente)
            cliente = prospecto.nombre + " " + prospecto.apellido_paterno + " " + prospecto.apellido_materno
            
            evento = Evento.objects.create(nombre=nombre,
                                           tipo=tipo,
                                           cliente=cliente,
                                           telefono_cliente=telefono_cliente,
                                           observaciones=observaciones,
                                           asesor=Asesor.objects.get(nombre=asesor),
                                           fecha_hora=make_aware(datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M")),
                                           lead=lead,
                                           tiempo_evento=tiempo_evento
                                           )
            Historial.objects.create(lead=lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se creó un evento. Nombre: {nombre}. Tipo: {tipo}. Observaciones: {observaciones}",
                                    )
            return JsonResponse(evento.pk, safe=False)
    
        if request.POST.get("select_accion"):
            accion = request.POST.get("select_accion")
            try:
                if accion == "Separar":
                    vehiculo = VehiculosInteresLead.objects.get(lead=lead, separado=True)
                elif accion == "Facturar":
                    vehiculo = VehiculosInteresLead.objects.get(lead=lead, facturado=True)
                elif accion == "Mostrar":
                    vehiculo = VehiculosInteresLead.objects.get(lead=lead, mostrado=True)
                print("vehiculo")
                print(vehiculo)
                vehiculo = f"{vehiculo.marca} {vehiculo.modelo}"
                return JsonResponse(vehiculo, safe=False)
            except:
                return JsonResponse(None, safe=False)

class OperativoAnfitrionView(LoginRequiredMixin, TemplateView):
    # Vista de Operativo Anfitrion

    template_name = "OperativoAnfitrion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        
        leads = Lead.objects.filter(activo=True, nombre_asesor__isnull=False).order_by("-id")

        functions.verificar_primer_contacto_todos_los_leads(leads)
        
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads_agendados = Lead.objects.filter(nombre_asesor__isnull=False, activo=True).exclude(etapa="Desistido").order_by("-id")
        leads_primer_contacto = Lead.objects.filter(nombre_asesor__isnull=True, activo=True).exclude(estado="Desistido").order_by("-id")

        verificaciones = HistorialVerificaciones.objects.select_related("lead").order_by("-id")

        mostrado_marcas = VehiculosInteresLead.objects.filter(mostrado=True).values("lead").distinct().values("lead", "marca", "modelo")


        anfitriones_agendados = leads_agendados.order_by("nombre_anfitrion").values("nombre_anfitrion").distinct()
        tipos_solicitud_agendados = leads_agendados.order_by("tipo_solicitud_verificacion").values("tipo_solicitud_verificacion").distinct()
        asesores_agendados = leads_agendados.order_by("nombre_asesor").values("nombre_asesor").distinct()
        salas_agendados = leads_agendados.order_by("sala").values("sala").distinct()

        
        if (leads_agendados.count() % 15) == 0:
            cantidad_agendados_pag = leads_agendados.count() // 15
        else:
            cantidad_agendados_pag = leads_agendados.count() // 15 + 1
        if (leads_primer_contacto.count() % 15) == 0:
            cantidad_primer_contacto_pag = leads_primer_contacto.count() // 15
        else:
            cantidad_primer_contacto_pag = leads_primer_contacto.count() // 15 + 1

        context["anfitriones_agendados"] = anfitriones_agendados
        context["asesores_agendados"] = asesores_agendados
        context["asesor_actual"] = asesor_actual
        context["calendario_general"] = calendario_general
        context["cantidad_agendados"] = leads_agendados.count()
        context["cantidad_verificados"] = verificaciones.count()
        context["cantidad_primer_contacto"] = leads_primer_contacto.count()
        context["cantidad_agendados_pag"] = cantidad_agendados_pag
        context["cantidad_primer_contacto_pag"] = cantidad_primer_contacto_pag
        context["cantidad_verificacion_pag"] = verificaciones.count() // 15 + 1
        context["leads_agendados"] = leads_agendados[0:15]
        context["leads_primer_contacto"] = leads_primer_contacto[0:15]
        context["mostrado_marcas"] = mostrado_marcas
        context["pages_agendados"] = 1
        context["pages_primer_contacto"] = 1
        context["pages_verificacion"] = 1
        context["salas_agendados"] = salas_agendados
        context["tipos_solicitud_agendados"] = tipos_solicitud_agendados
        context["user"] = user
        context["verificaciones"] = verificaciones[0:15]

        return context
    

    def post(self, request):
        leads = Lead.objects.all()

        desde_primer_contacto = request.POST.get("desde_primer_contacto")
        hasta_primer_contacto = request.POST.get("hasta_primer_contacto")

        try:
            json.loads(request.POST.get("if_filtrar_primer_contacto"))
            if_filtrar_primer_contacto = True
        except:
            if_filtrar_primer_contacto = False
        if if_filtrar_primer_contacto:
            if desde_primer_contacto:
                desde_primer_contacto = datetime.strptime(desde_primer_contacto, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_primer_contacto)
            if hasta_primer_contacto:
                hasta_primer_contacto = datetime.strptime(hasta_primer_contacto, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_primer_contacto)

        desde_verificacion = request.POST.get("desde_verificacion")
        hasta_verificacion = request.POST.get("hasta_verificacion")

        try:
            json.loads(request.POST.get("if_filtrar_verificacion"))
            if_filtrar_verificacion = True
        except:
            if_filtrar_verificacion = False

        if if_filtrar_verificacion:
            if desde_verificacion:
                desde_verificacion = datetime.strptime(desde_verificacion, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_verificacion)
            if hasta_verificacion:
                hasta_verificacion = datetime.strptime(hasta_verificacion, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_verificacion)

        anfitrion_agendados = request.POST.get("anfitrion_agendados")
        verificado_agendados = request.POST.get("verificado_agendados")
        tipo_solicitud_agendados = request.POST.get("tipo_solicitud_agendados")
        asesor_agendados = request.POST.get("asesor_agendados")
        sala_agendados = request.POST.get("sala_agendados")
        desde_agendados = request.POST.get("desde_agendados")
        hasta_agendados = request.POST.get("hasta_agendados")
        search_agendados = request.POST.get("search_agendados")

        try:
            json.loads(request.POST.get("if_filtrar_agendados"))
            if_filtrar_agendados = True
        except:
            if_filtrar_agendados = False

        if if_filtrar_agendados:
            if anfitrion_agendados:
                leads = leads.filter(nombre_anfitrion=anfitrion_agendados)
            if verificado_agendados:
                if verificado_agendados == "SI":
                    leads = leads.filter(estado_llamada_verificacion__isnull=False)
                elif verificado_agendados == "NO":
                    leads = leads.filter(estado_llamada_verificacion__isnull=True)
            if tipo_solicitud_agendados:
                leads = leads.filter(tipo_solicitud_verificacion=tipo_solicitud_agendados)
            if asesor_agendados:
                leads = leads.filter(nombre_asesor=asesor_agendados)
            if sala_agendados:
                leads = leads.filter(sala=sala_agendados)
            if desde_agendados:
                desde_agendados = datetime.strptime(desde_agendados, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_agendados)
            if hasta_agendados:
                hasta_agendados = datetime.strptime(hasta_agendados, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_agendados)
            if search_agendados:
                leads = leads.filter(prospecto__nombre__icontains=search_agendados) | leads.filter(prospecto__celular__icontains=search_agendados)

        if request.POST.get("pages_primer_contacto"):
            page_min = (int(request.POST.get("pages_primer_contacto")) - 1) * 15
            page_max = int(request.POST.get("pages_primer_contacto")) * 15
            leads_primer_contacto = leads.filter(nombre_asesor__isnull=True, activo=True).order_by("-id")[page_min:page_max]
            leads_primer_contacto = list(leads_primer_contacto.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_primer_contacto, safe=False)
        if request.POST.get("pages_verificacion"):
            page_min = (int(request.POST.get("pages_verificacion")) - 1) * 15
            page_max = int(request.POST.get("pages_verificacion")) * 15
            verificaciones = HistorialVerificaciones.objects.select_related("lead").order_by("-id")[page_min:page_max]
            verificaciones = list(verificaciones.values("id", "fecha_hora_verificacion", "lead__prospecto__nombre", "responsable", "lead__prospecto__celular", "lead__origen_lead", "estado_llamada", "lead__nombre_anfitrion", "tipo_solicitud", "lead__sala", "lead__prospecto__nombre_asesor", "lead__comentario"))
            return JsonResponse(verificaciones, safe=False)
        if request.POST.get("pages_agendados"):
            page_min = (int(request.POST.get("pages_agendados")) - 1) * 15
            page_max = int(request.POST.get("pages_agendados")) * 15
            leads_agendados = leads.filter(nombre_asesor__isnull=False, activo=True).exclude(etapa="Desistido").order_by("-id")[page_min:page_max]
            leads_agendados = list(leads_agendados.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion", "tipo_solicitud_verificacion", "prospecto__nombre_asesor"))
            return JsonResponse(leads_agendados, safe=False)
        if request.POST.get("filtrar_primer_contacto"):
            page_min = 0
            page_max = 15
            desde_primer_contacto = request.POST.get("desde_primer_contacto")
            hasta_primer_contacto = request.POST.get("hasta_primer_contacto")

            leads_primer_contacto = Lead.objects.filter(nombre_asesor__isnull=True, activo=True).order_by("-id")
            
            if desde_primer_contacto:
                desde_primer_contacto = datetime.strptime(desde_primer_contacto, '%Y-%m-%d').date()
                leads_primer_contacto = leads_primer_contacto.filter(fecha_apertura__gte=desde_primer_contacto)
            if hasta_primer_contacto:
                hasta_primer_contacto = datetime.strptime(hasta_primer_contacto, '%Y-%m-%d').date()
                leads_primer_contacto = leads_primer_contacto.filter(fecha_apertura__lte=hasta_primer_contacto)

            print(leads_primer_contacto)

            if (leads_primer_contacto.count() % 15) == 0:
                cantidad_filtrado_pag = leads_primer_contacto.count() // 15
            else:
                cantidad_filtrado_pag = leads_primer_contacto.count() // 15 + 1

            leads_primer_contacto = leads_primer_contacto[page_min:page_max]
            
            leads_primer_contacto = list(leads_primer_contacto.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_primer_contacto.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_primer_contacto)
            return JsonResponse(leads_primer_contacto, safe=False)
        if request.POST.get("filtrar_verificacion"):
            page_min = 0
            page_max = 15
            desde_verificacion = request.POST.get("desde_verificacion")
            hasta_verificacion = request.POST.get("hasta_verificacion")

            verificaciones = HistorialVerificaciones.objects.select_related("lead").order_by("-id")
            
            if desde_verificacion:
                desde_verificacion = datetime.strptime(desde_verificacion, '%Y-%m-%d').date()
                verificaciones = verificaciones.filter(fecha_hora_verificacion__gte=desde_verificacion)
            if hasta_verificacion:
                hasta_verificacion = datetime.strptime(hasta_verificacion, '%Y-%m-%d').date()
                verificaciones = verificaciones.filter(fecha_hora_verificacion__lte=hasta_verificacion)

            print(verificaciones)

            if (verificaciones.count() % 15) == 0:
                cantidad_filtrado_pag = verificaciones.count() // 15
            else:
                cantidad_filtrado_pag = verificaciones.count() // 15 + 1

            verificaciones = verificaciones[page_min:page_max]
            
            verificaciones = list(verificaciones.values("id", "fecha_hora_verificacion", "lead__prospecto__nombre", "responsable", "lead__prospecto__celular", "lead__origen_lead", "estado_llamada", "lead__nombre_anfitrion", "tipo_solicitud", "lead__sala", "lead__prospecto__nombre_asesor"))
            verificaciones.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(verificaciones)
            return JsonResponse(verificaciones, safe=False)
        if request.POST.get("filtrar_agendados"):
            page_min = 0
            page_max = 15
            anfitrion_agendados = request.POST.get("anfitrion_agendados")
            verificado_agendados = request.POST.get("verificado_agendados")
            tipo_solicitud_agendados = request.POST.get("tipo_solicitud_agendados")
            asesor_agendados = request.POST.get("asesor_agendados")
            sala_agendados = request.POST.get("sala_agendados")
            desde_agendados = request.POST.get("desde_agendados")
            hasta_agendados = request.POST.get("hasta_agendados")
            search_agendados = request.POST.get("search_agendados")

            leads_agendados = Lead.objects.filter(nombre_asesor__isnull=False, activo=True).exclude(etapa="Desistido").order_by("-id")
            
            if anfitrion_agendados:
                leads_agendados = leads_agendados.filter(nombre_anfitrion=anfitrion_agendados)
            if verificado_agendados:
                if verificado_agendados == "SI":
                    leads_agendados = leads_agendados.filter(estado_llamada_verificacion__isnull=False)
                elif verificado_agendados == "NO":
                    leads_agendados = leads_agendados.filter(estado_llamada_verificacion__isnull=True)
            if tipo_solicitud_agendados:
                leads_agendados = leads_agendados.filter(tipo_solicitud_verificacion=tipo_solicitud_agendados)
            if asesor_agendados:
                leads_agendados = leads_agendados.filter(nombre_asesor=asesor_agendados)
            if sala_agendados:
                leads_agendados = leads_agendados.filter(sala=sala_agendados)
            if desde_agendados:
                desde_agendados = datetime.strptime(desde_agendados, '%Y-%m-%d').date()
                leads_agendados = leads_agendados.filter(fecha_apertura__gte=desde_agendados)
            if hasta_agendados:
                hasta_agendados = datetime.strptime(hasta_agendados, '%Y-%m-%d').date()
                leads_agendados = leads_agendados.filter(fecha_apertura__lte=hasta_agendados)
            if search_agendados:
                leads_agendados = leads_agendados.filter(prospecto__nombre__icontains=search_agendados) | leads_agendados.filter(prospecto__celular__icontains=search_agendados)

            print(leads_agendados)
            
            if (leads_agendados.count() % 15) == 0:
                cantidad_filtrado_pag = leads_agendados.count() // 15
            else:
                cantidad_filtrado_pag = leads_agendados.count() // 15 + 1

            leads_agendados = leads_agendados[page_min:page_max]
            
            leads_agendados = list(leads_agendados.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_agendados.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            return JsonResponse(leads_agendados, safe=False)

class OperativoAsesorView(LoginRequiredMixin, TemplateView):
    # Vista de Operativo Asesor

    template_name = "OperativoAsesor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0
        
        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads = Lead.objects.filter(activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")

        #functions.verificar_primer_contacto_todos_los_leads(leads)

        if calendario_general == False:
            leads_no_contactado = Lead.objects.filter(etapa="No contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            leads_contactado = Lead.objects.filter(etapa="Contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            leads_seguimiento = Lead.objects.filter(etapa="Seguimiento", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            leads_anticipo = Lead.objects.filter(etapa="Anticipo", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            leads_conversion = Lead.objects.filter(etapa="Conversión", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
        else:

            leads_no_contactado = Lead.objects.filter(etapa="No contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            leads_contactado = Lead.objects.filter(etapa="Contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            leads_seguimiento = Lead.objects.filter(etapa="Seguimiento", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            leads_anticipo = Lead.objects.filter(etapa="Anticipo", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            leads_conversion = Lead.objects.filter(etapa="Conversión", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
        respuestas = CatalogoRespuestasByEtapa.objects.all()
        estados = CatalogoRespuestasByEtapa.objects.all()

        mostrado_marcas = VehiculosInteresLead.objects.filter(mostrado=True).values("lead", "mostrado").distinct().annotate(latest=Max("id")).values("lead", "marca", "modelo")

        origenes_lead_no_contactado = leads_no_contactado.order_by("origen_lead").values("origen_lead").distinct()
        origenes_lead_contactado = leads_contactado.order_by("origen_lead").values("origen_lead").distinct()
        origenes_lead_seguimiento = leads_seguimiento.order_by("origen_lead").values("origen_lead").distinct()
        origenes_lead_anticipo = leads_anticipo.order_by("origen_lead").values("origen_lead").distinct()
        origenes_lead_conversion = leads_conversion.order_by("origen_lead").values("origen_lead").distinct()

        respuestas_no_contactado = leads_no_contactado.order_by("respuesta").values("respuesta").distinct()
        respuestas_contactado = leads_contactado.order_by("respuesta").values("respuesta").distinct()
        respuestas_seguimiento = leads_seguimiento.order_by("respuesta").values("respuesta").distinct()
        respuestas_anticipo = leads_anticipo.order_by("respuesta").values("respuesta").distinct()
        respuestas_conversion = leads_conversion.order_by("respuesta").values("respuesta").distinct()

        estados_no_contactado = leads_no_contactado.order_by("estado").values("estado").distinct()
        estados_contactado = leads_contactado.order_by("estado").values("estado").distinct()
        estados_seguimiento = leads_seguimiento.order_by("estado").values("estado").distinct()
        estados_anticipo = leads_anticipo.order_by("estado").values("estado").distinct()
        estados_conversion = leads_conversion.order_by("estado").values("estado").distinct()

        asesores_no_contactado = leads_no_contactado.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_contactado = leads_contactado.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_seguimiento = leads_seguimiento.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_anticipo = leads_anticipo.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_conversion = leads_conversion.order_by("nombre_asesor").values("nombre_asesor").distinct()

        salas_no_contactado = leads_no_contactado.order_by("sala").values("sala").distinct()
        salas_contactado = leads_contactado.order_by("sala").values("sala").distinct()
        salas_seguimiento = leads_seguimiento.order_by("sala").values("sala").distinct()
        salas_anticipo = leads_anticipo.order_by("sala").values("sala").distinct()
        salas_conversion = leads_conversion.order_by("sala").values("sala").distinct()

        marcas_no_contactado = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_no_contactado).values("marca").distinct()
        marcas_contactado = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_contactado).values("marca").distinct()
        marcas_seguimiento = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_seguimiento).values("marca").distinct()
        marcas_anticipo = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_anticipo).values("marca").distinct()
        marcas_conversion = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_conversion).values("marca").distinct()

        modelos_no_contactado = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_no_contactado).values("modelo").distinct() 
        modelos_contactado = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_contactado).values("modelo").distinct() 
        modelos_seguimiento = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_seguimiento).values("modelo").distinct() 
        modelos_anticipo = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_anticipo).values("modelo").distinct() 
        modelos_conversion = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_conversion).values("modelo").distinct() 

        if (leads_no_contactado.count() % 15) == 0:
            cantidad_no_contactado_pag = leads_no_contactado.count() // 15
        else:
            cantidad_no_contactado_pag = leads_no_contactado.count() // 15 + 1

        if (leads_contactado.count() % 15) == 0:
            cantidad_contactado_pag = leads_contactado.count() // 15
        else:
            cantidad_contactado_pag = leads_contactado.count() // 15 + 1

        if (leads_seguimiento.count() % 15) == 0:
            cantidad_seguimiento_pag = leads_seguimiento.count() // 15
        else:
            cantidad_seguimiento_pag = leads_seguimiento.count() // 15 + 1

        if (leads_anticipo.count() % 15) == 0:
            cantidad_anticipo_pag = leads_anticipo.count() // 15
        else:
            cantidad_anticipo_pag = leads_anticipo.count() // 15 + 1

        if (leads_conversion.count() % 15) == 0:
            cantidad_conversion_pag = leads_conversion.count() // 15
        else:
            cantidad_conversion_pag = leads_conversion.count() // 15 + 1

        context["asesor_actual"] = asesor_actual
        context["asesores_no_contactado"] = asesores_no_contactado
        context["asesores_contactado"] = asesores_contactado
        context["asesores_seguimiento"] = asesores_seguimiento
        context["asesores_anticipo"] = asesores_anticipo
        context["asesores_conversion"] = asesores_conversion
        context["calendario_general"] = calendario_general
        context["cantidad_no_contactado"] = leads_no_contactado.count()
        context["cantidad_contactado"] = leads_contactado.count()
        context["cantidad_seguimiento"] = leads_seguimiento.count()
        context["cantidad_anticipo"] = leads_anticipo.count()
        context["cantidad_conversion"] = leads_conversion.count()
        context["cantidad_no_contactado_pag"] = cantidad_no_contactado_pag
        context["cantidad_contactado_pag"] = cantidad_contactado_pag
        context["cantidad_seguimiento_pag"] = cantidad_seguimiento_pag
        context["cantidad_anticipo_pag"] = cantidad_anticipo_pag
        context["cantidad_conversion_pag"] = cantidad_conversion_pag
        context["estados"] = estados
        context["estados_no_contactado"] = estados_no_contactado
        context["estados_contactado"] = estados_contactado
        context["estados_seguimiento"] = estados_seguimiento
        context["estados_anticipo"] = estados_anticipo
        context["estados_conversion"] = estados_conversion
        context["leads_no_contactado"] = leads_no_contactado[0:15]
        context["leads_contactado"] = leads_contactado[0:15]
        context["leads_seguimiento"] = leads_seguimiento[0:15]
        context["leads_anticipo"] = leads_anticipo[0:15]
        context["leads_conversion"] = leads_conversion[0:15]
        context["marcas_no_contactado"] = marcas_no_contactado
        context["marcas_contactado"] = marcas_contactado
        context["marcas_seguimiento"] = marcas_seguimiento
        context["marcas_anticipo"] = marcas_anticipo
        context["marcas_conversion"] = marcas_conversion
        context["modelos_no_contactado"] = modelos_no_contactado
        context["modelos_contactado"] = modelos_contactado
        context["modelos_seguimiento"] = modelos_seguimiento
        context["modelos_anticipo"] = modelos_anticipo
        context["modelos_conversion"] = modelos_conversion
        context["mostrado_marcas"] = mostrado_marcas
        context["origenes_lead_no_contactado"] = origenes_lead_no_contactado
        context["origenes_lead_contactado"] = origenes_lead_contactado
        context["origenes_lead_seguimiento"] = origenes_lead_seguimiento
        context["origenes_lead_anticipo"] = origenes_lead_anticipo
        context["origenes_lead_conversion"] = origenes_lead_conversion
        context["pages_no_contactado"] = 1
        context["pages_contactado"] = 1
        context["pages_seguimiento"] = 1
        context["pages_anticipo"] = 1
        context["pages_conversion"] = 1
        context["respuestas"] = respuestas
        context["respuestas_no_contactado"] = respuestas_no_contactado
        context["respuestas_contactado"] = respuestas_contactado
        context["respuestas_seguimiento"] = respuestas_seguimiento
        context["respuestas_anticipo"] = respuestas_anticipo
        context["respuestas_conversion"] = respuestas_conversion
        context["salas_no_contactado"] = salas_no_contactado
        context["salas_contactado"] = salas_contactado
        context["salas_seguimiento"] = salas_seguimiento
        context["salas_anticipo"] = salas_anticipo
        context["salas_conversion"] = salas_conversion
        context["user"] = user

        return context
    
    def post(self, request):

        user = User.objects.get(username=self.request.user)
        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads = Lead.objects.all()

        origen_lead_no_contactado = request.POST.get("origen_lead_no_contactado")
        respuesta_no_contactado = request.POST.get("respuesta_no_contactado")
        estado_no_contactado = request.POST.get("estado_no_contactado")
        asesor_no_contactado = request.POST.get("asesor_no_contactado")
        sala_no_contactado = request.POST.get("sala_no_contactado")
        marca_no_contactado = request.POST.get("marca_no_contactado")
        modelo_no_contactado = request.POST.get("modelo_no_contactado")
        desde_no_contactado = request.POST.get("desde_no_contactado")
        hasta_no_contactado = request.POST.get("hasta_no_contactado")
        search_no_contactado = request.POST.get("search_no_contactado")

        try:
            json.loads(request.POST.get("if_filtrar_no_contactado"))
            if_filtrar_no_contactado = True
        except:
            if_filtrar_no_contactado = False

        if if_filtrar_no_contactado:
            if origen_lead_no_contactado:
                leads = leads.filter(origen_lead=origen_lead_no_contactado)
            if respuesta_no_contactado:
                leads = leads.filter(respuesta=respuesta_no_contactado)
            if estado_no_contactado:
                leads = leads.filter(estado=estado_no_contactado)
            if asesor_no_contactado:
                leads = leads.filter(nombre_asesor=asesor_no_contactado)
            if sala_no_contactado:
                leads = leads.filter(sala=sala_no_contactado)
            if desde_no_contactado:
                desde_no_contactado = datetime.strptime(desde_no_contactado, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_no_contactado)
            if hasta_no_contactado:
                hasta_no_contactado = datetime.strptime(hasta_no_contactado, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_no_contactado)
            if search_no_contactado:
                leads = leads.filter(prospecto__nombre__icontains=search_no_contactado) | leads.filter(prospecto__celular__icontains=search_no_contactado)

        origen_lead_contactado = request.POST.get("origen_lead_contactado")
        respuesta_contactado = request.POST.get("respuesta_contactado")
        estado_contactado = request.POST.get("estado_contactado")
        asesor_contactado = request.POST.get("asesor_contactado")
        sala_contactado = request.POST.get("sala_contactado")
        marca_contactado = request.POST.get("marca_contactado")
        modelo_contactado = request.POST.get("modelo_contactado")
        desde_contactado = request.POST.get("desde_contactado")
        hasta_contactado = request.POST.get("hasta_contactado")
        search_contactado = request.POST.get("search_contactado")

        try:
            json.loads(request.POST.get("if_filtrar_contactado"))
            if_filtrar_contactado = True
        except:
            if_filtrar_contactado = False

        if if_filtrar_contactado:
            if origen_lead_contactado:
                leads = leads.filter(origen_lead=origen_lead_contactado)
            if respuesta_contactado:
                leads = leads.filter(respuesta=respuesta_contactado)
            if estado_contactado:
                leads = leads.filter(estado=estado_contactado)
            if asesor_contactado:
                leads = leads.filter(nombre_asesor=asesor_contactado)
            if sala_contactado:
                leads = leads.filter(sala=sala_contactado)
            if desde_contactado:
                desde_contactado = datetime.strptime(desde_contactado, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_contactado)
            if hasta_contactado:
                hasta_contactado = datetime.strptime(hasta_contactado, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_contactado)
            if search_contactado:
                leads = leads.filter(prospecto__nombre__icontains=search_contactado) | leads.filter(prospecto__celular__icontains=search_contactado)

        origen_lead_seguimiento = request.POST.get("origen_lead_seguimiento")
        respuesta_seguimiento = request.POST.get("respuesta_seguimiento")
        estado_seguimiento = request.POST.get("estado_seguimiento")
        asesor_seguimiento = request.POST.get("asesor_seguimiento")
        sala_seguimiento = request.POST.get("sala_seguimiento")
        marca_seguimiento = request.POST.get("marca_seguimiento")
        modelo_seguimiento = request.POST.get("modelo_seguimiento")
        desde_seguimiento = request.POST.get("desde_seguimiento")
        hasta_seguimiento = request.POST.get("hasta_seguimiento")
        search_seguimiento = request.POST.get("search_seguimiento")

        try:
            json.loads(request.POST.get("if_filtrar_seguimiento"))
            if_filtrar_seguimiento = True
        except:
            if_filtrar_seguimiento = False

        if if_filtrar_seguimiento:
            if origen_lead_seguimiento:
                leads = leads.filter(origen_lead=origen_lead_seguimiento)
            if respuesta_seguimiento:
                leads = leads.filter(respuesta=respuesta_seguimiento)
            if estado_seguimiento:
                leads = leads.filter(estado=estado_seguimiento)
            if asesor_seguimiento:
                leads = leads.filter(nombre_asesor=asesor_seguimiento)
            if sala_seguimiento:
                leads = leads.filter(sala=sala_seguimiento)
            if desde_seguimiento:
                desde_seguimiento = datetime.strptime(desde_seguimiento, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_seguimiento)
            if hasta_seguimiento:
                hasta_seguimiento = datetime.strptime(hasta_seguimiento, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_seguimiento)
            if search_seguimiento:
                leads = leads.filter(prospecto__nombre__icontains=search_seguimiento) | leads.filter(prospecto__celular__icontains=search_seguimiento)

        origen_lead_anticipo = request.POST.get("origen_lead_anticipo")
        respuesta_anticipo = request.POST.get("respuesta_anticipo")
        estado_anticipo = request.POST.get("estado_anticipo")
        asesor_anticipo = request.POST.get("asesor_anticipo")
        sala_anticipo = request.POST.get("sala_anticipo")
        marca_anticipo = request.POST.get("marca_anticipo")
        modelo_anticipo = request.POST.get("modelo_anticipo")
        desde_anticipo = request.POST.get("desde_anticipo")
        hasta_anticipo = request.POST.get("hasta_anticipo")
        search_anticipo = request.POST.get("search_anticipo")

        try:
            json.loads(request.POST.get("if_filtrar_anticipo"))
            if_filtrar_anticipo = True
        except:
            if_filtrar_anticipo = False

        if if_filtrar_anticipo:
            if origen_lead_anticipo:
                leads = leads.filter(origen_lead=origen_lead_anticipo)
            if respuesta_anticipo:
                leads = leads.filter(respuesta=respuesta_anticipo)
            if estado_anticipo:
                leads = leads.filter(estado=estado_anticipo)
            if asesor_anticipo:
                leads = leads.filter(nombre_asesor=asesor_anticipo)
            if sala_anticipo:
                leads = leads.filter(sala=sala_anticipo)
            if desde_anticipo:
                desde_anticipo = datetime.strptime(desde_anticipo, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_anticipo)
            if hasta_anticipo:
                hasta_anticipo = datetime.strptime(hasta_anticipo, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_anticipo)
            if search_anticipo:
                leads = leads.filter(prospecto__nombre__icontains=search_anticipo) | leads.filter(prospecto__celular__icontains=search_anticipo)

        origen_lead_conversion = request.POST.get("origen_lead_conversion")
        respuesta_conversion = request.POST.get("respuesta_conversion")
        estado_conversion = request.POST.get("estado_conversion")
        asesor_conversion = request.POST.get("asesor_conversion")
        sala_conversion = request.POST.get("sala_conversion")
        marca_conversion = request.POST.get("marca_conversion")
        modelo_conversion = request.POST.get("modelo_conversion")
        desde_conversion = request.POST.get("desde_conversion")
        hasta_conversion = request.POST.get("hasta_conversion")
        search_conversion = request.POST.get("search_conversion")

        try:
            json.loads(request.POST.get("if_filtrar_conversion"))
            if_filtrar_conversion = True
        except:
            if_filtrar_conversion = False

        if if_filtrar_conversion:
            if origen_lead_conversion:
                leads = leads.filter(origen_lead=origen_lead_conversion)
            if respuesta_conversion:
                leads = leads.filter(respuesta=respuesta_conversion)
            if estado_conversion:
                leads = leads.filter(estado=estado_conversion)
            if asesor_conversion:
                leads = leads.filter(nombre_asesor=asesor_conversion)
            if sala_conversion:
                leads = leads.filter(sala=sala_conversion)
            if desde_conversion:
                desde_conversion = datetime.strptime(desde_conversion, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_conversion)
            if hasta_conversion:
                hasta_conversion = datetime.strptime(hasta_conversion, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_conversion)
            if search_conversion:
                leads = leads.filter(prospecto__nombre__icontains=search_conversion) | leads.filter(prospecto__celular__icontains=search_conversion)

        if request.POST.get("pages_no_contactado"):
            page_min = (int(request.POST.get("pages_no_contactado")) - 1) * 15
            page_max = int(request.POST.get("pages_no_contactado")) * 15
            if calendario_general == False:
                leads_no_contactado = leads.filter(etapa="No contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")[page_min:page_max]
            else:
                leads_no_contactado = leads.filter(etapa="No contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")[page_min:page_max]
            leads_no_contactado = list(leads_no_contactado.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_no_contactado, safe=False)
        if request.POST.get("pages_contactado"):
            page_min = (int(request.POST.get("pages_contactado")) - 1) * 15
            page_max = int(request.POST.get("pages_contactado")) * 15
            if calendario_general == False:
                leads_contactado = leads.filter(etapa="Contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")[page_min:page_max]
            else:
                leads_contactado = leads.filter(etapa="Contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")[page_min:page_max]
            leads_contactado = list(leads_contactado.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_contactado, safe=False)
        if request.POST.get("pages_seguimiento"):
            page_min = (int(request.POST.get("pages_seguimiento")) - 1) * 15
            page_max = int(request.POST.get("pages_seguimiento")) * 15
            if calendario_general == False:
                leads_seguimiento = leads.filter(etapa="Seguimiento", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")[page_min:page_max]
            else:
                leads_seguimiento = leads.filter(etapa="Seguimiento", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")[page_min:page_max]
            leads_seguimiento = list(leads_seguimiento.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_seguimiento, safe=False)
        if request.POST.get("pages_anticipo"):
            page_min = (int(request.POST.get("pages_anticipo")) - 1) * 15
            page_max = int(request.POST.get("pages_anticipo")) * 15
            if calendario_general == False:
                leads_anticipo = leads.filter(etapa="Anticipo", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")[page_min:page_max]
            else:
                leads_anticipo = leads.filter(etapa="Anticipo", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")[page_min:page_max]
            leads_anticipo = list(leads_anticipo.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_anticipo, safe=False)
        if request.POST.get("pages_conversion"):
            page_min = (int(request.POST.get("pages_conversion")) - 1) * 15
            page_max = int(request.POST.get("pages_conversion")) * 15
            if calendario_general == False:
                leads_conversion = leads.filter(etapa="Conversión", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")[page_min:page_max]
            else:
                leads_conversion = leads.filter(etapa="Conversión", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")[page_min:page_max]
            leads_conversion = list(leads_conversion.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            return JsonResponse(leads_conversion, safe=False)
        if request.POST.get("filtrar_no_contactado"):
            page_min = 0
            page_max = 15
            origen_lead_no_contactado = request.POST.get("origen_lead_no_contactado")
            respuesta_no_contactado = request.POST.get("respuesta_no_contactado")
            estado_no_contactado = request.POST.get("estado_no_contactado")
            asesor_no_contactado = request.POST.get("asesor_no_contactado")
            sala_no_contactado = request.POST.get("sala_no_contactado")
            marca_no_contactado = request.POST.get("marca_no_contactado")
            modelo_no_contactado = request.POST.get("modelo_no_contactado")
            desde_no_contactado = request.POST.get("desde_no_contactado")
            hasta_no_contactado = request.POST.get("hasta_no_contactado")
            search_no_contactado = request.POST.get("search_no_contactado")

            if calendario_general == False:
                leads_no_contactado = Lead.objects.filter(etapa="No contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            else:
                leads_no_contactado = Lead.objects.filter(etapa="No contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            
            if origen_lead_no_contactado:
                leads_no_contactado = leads_no_contactado.filter(origen_lead=origen_lead_no_contactado)
            if respuesta_no_contactado:
                leads_no_contactado = leads_no_contactado.filter(respuesta=respuesta_no_contactado)
            if estado_no_contactado:
                leads_no_contactado = leads_no_contactado.filter(estado=estado_no_contactado)
            if asesor_no_contactado:
                leads_no_contactado = leads_no_contactado.filter(nombre_asesor=asesor_no_contactado)
            if sala_no_contactado:
                leads_no_contactado = leads_no_contactado.filter(sala=sala_no_contactado)
            if desde_no_contactado:
                desde_no_contactado = datetime.strptime(desde_no_contactado, '%Y-%m-%d').date()
                leads_no_contactado = leads_no_contactado.filter(fecha_apertura__gte=desde_no_contactado)
            if hasta_no_contactado:
                hasta_no_contactado = datetime.strptime(hasta_no_contactado, '%Y-%m-%d').date()
                leads_no_contactado = leads_no_contactado.filter(fecha_apertura__lte=hasta_no_contactado)
            if search_no_contactado:
                # Descomponemos el valor de búsqueda en posibles partes (nombre, segundo nombre o apellido)
                search_terms = search_no_contactado.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_no_contactado = leads_no_contactado.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_no_contactado = leads_no_contactado.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_no_contactado = leads_no_contactado.filter(
                        Q(prospecto__nombre__icontains=search_no_contactado) |
                        Q(prospecto__apellido_paterno__icontains=search_no_contactado) |
                        Q(prospecto__apellido_materno__icontains=search_no_contactado) |
                        Q(prospecto__celular__icontains=search_no_contactado)
                    )

            if (leads_no_contactado.count() % 15) == 0:
                cantidad_filtrado_pag = leads_no_contactado.count() // 15
            else:
                cantidad_filtrado_pag = leads_no_contactado.count() // 15 + 1


            leads_no_contactado = leads_no_contactado[page_min:page_max]
            
            leads_no_contactado = list(leads_no_contactado.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_no_contactado.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_no_contactado)
            return JsonResponse(leads_no_contactado, safe=False)

        if request.POST.get("filtrar_contactado"):
            page_min = 0
            page_max = 15
            origen_lead_contactado = request.POST.get("origen_lead_contactado")
            respuesta_contactado = request.POST.get("respuesta_contactado")
            estado_contactado = request.POST.get("estado_contactado")
            asesor_contactado = request.POST.get("asesor_contactado")
            sala_contactado = request.POST.get("sala_contactado")
            marca_contactado = request.POST.get("marca_contactado")
            modelo_contactado = request.POST.get("modelo_contactado")
            desde_contactado = request.POST.get("desde_contactado")
            hasta_contactado = request.POST.get("hasta_contactado")
            search_contactado = request.POST.get("search_contactado")

            if calendario_general == False:
                leads_contactado = Lead.objects.filter(etapa="Contactado", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            else:
                leads_contactado = Lead.objects.filter(etapa="Contactado", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            
            if origen_lead_contactado:
                leads_contactado = leads_contactado.filter(origen_lead=origen_lead_contactado)
            if respuesta_contactado:
                leads_contactado = leads_contactado.filter(respuesta=respuesta_contactado)
            if estado_contactado:
                leads_contactado = leads_contactado.filter(estado=estado_contactado)
            if asesor_contactado:
                leads_contactado = leads_contactado.filter(nombre_asesor=asesor_contactado)
            if sala_contactado:
                leads_contactado = leads_contactado.filter(sala=sala_contactado)
            if desde_contactado:
                desde_contactado = datetime.strptime(desde_contactado, '%Y-%m-%d').date()
                leads_contactado = leads_contactado.filter(fecha_apertura__gte=desde_contactado)
            if hasta_contactado:
                hasta_contactado = datetime.strptime(hasta_contactado, '%Y-%m-%d').date()
                leads_contactado = leads_contactado.filter(fecha_apertura__lte=hasta_contactado)
            if search_contactado:
                search_terms = search_contactado.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_contactado = leads_contactado.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_contactado = leads_contactado.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_contactado = leads_contactado.filter(
                        Q(prospecto__nombre__icontains=search_contactado) |
                        Q(prospecto__apellido_paterno__icontains=search_contactado) |
                        Q(prospecto__apellido_materno__icontains=search_contactado) |
                        Q(prospecto__celular__icontains=search_contactado)
                    )

            if (leads_contactado.count() % 15) == 0:
                cantidad_filtrado_pag = leads_contactado.count() // 15
            else:
                cantidad_filtrado_pag = leads_contactado.count() // 15 + 1

            leads_contactado = leads_contactado[page_min:page_max]
            
            leads_contactado = list(leads_contactado.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_contactado.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_contactado)
            return JsonResponse(leads_contactado, safe=False)
        
        if request.POST.get("filtrar_seguimiento"):
            page_min = 0
            page_max = 15
            origen_lead_seguimiento = request.POST.get("origen_lead_seguimiento")
            respuesta_seguimiento = request.POST.get("respuesta_seguimiento")
            estado_seguimiento = request.POST.get("estado_seguimiento")
            asesor_seguimiento = request.POST.get("asesor_seguimiento")
            sala_seguimiento = request.POST.get("sala_seguimiento")
            marca_seguimiento = request.POST.get("marca_seguimiento")
            modelo_seguimiento = request.POST.get("modelo_seguimiento")
            desde_seguimiento = request.POST.get("desde_seguimiento")
            hasta_seguimiento = request.POST.get("hasta_seguimiento")
            search_seguimiento = request.POST.get("search_seguimiento")

            if calendario_general == False:
                leads_seguimiento = Lead.objects.filter(etapa="Seguimiento", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            else:
                leads_seguimiento = Lead.objects.filter(etapa="Seguimiento", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            
            if origen_lead_seguimiento:
                leads_seguimiento = leads_seguimiento.filter(origen_lead=origen_lead_seguimiento)
            if respuesta_seguimiento:
                leads_seguimiento = leads_seguimiento.filter(respuesta=respuesta_seguimiento)
            if estado_seguimiento:
                leads_seguimiento = leads_seguimiento.filter(estado=estado_seguimiento)
            if asesor_seguimiento:
                leads_seguimiento = leads_seguimiento.filter(nombre_asesor=asesor_seguimiento)
            if sala_seguimiento:
                leads_seguimiento = leads_seguimiento.filter(sala=sala_seguimiento)
            if desde_seguimiento:
                desde_seguimiento = datetime.strptime(desde_seguimiento, '%Y-%m-%d').date()
                leads_seguimiento = leads_seguimiento.filter(fecha_apertura__gte=desde_seguimiento)
            if hasta_seguimiento:
                hasta_seguimiento = datetime.strptime(hasta_seguimiento, '%Y-%m-%d').date()
                leads_seguimiento = leads_seguimiento.filter(fecha_apertura__lte=hasta_seguimiento)
            if search_seguimiento:
                search_terms = search_seguimiento.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_seguimiento = leads_seguimiento.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_seguimiento = leads_seguimiento.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_seguimiento = leads_seguimiento.filter(
                        Q(prospecto__nombre__icontains=search_seguimiento) |
                        Q(prospecto__apellido_paterno__icontains=search_seguimiento) |
                        Q(prospecto__apellido_materno__icontains=search_seguimiento) |
                        Q(prospecto__celular__icontains=search_seguimiento)
                    )

            if (leads_seguimiento.count() % 15) == 0:
                cantidad_filtrado_pag = leads_seguimiento.count() // 15
            else:
                cantidad_filtrado_pag = leads_seguimiento.count() // 15 + 1

            leads_seguimiento = leads_seguimiento[page_min:page_max]
            
            leads_seguimiento = list(leads_seguimiento.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_seguimiento.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_seguimiento)
            return JsonResponse(leads_seguimiento, safe=False)
        
        if request.POST.get("filtrar_anticipo"):
            page_min = 0
            page_max = 15
            origen_lead_anticipo = request.POST.get("origen_lead_anticipo")
            respuesta_anticipo = request.POST.get("respuesta_anticipo")
            estado_anticipo = request.POST.get("estado_anticipo")
            asesor_anticipo = request.POST.get("asesor_anticipo")
            sala_anticipo = request.POST.get("sala_anticipo")
            marca_anticipo = request.POST.get("marca_anticipo")
            modelo_anticipo = request.POST.get("modelo_anticipo")
            desde_anticipo = request.POST.get("desde_anticipo")
            hasta_anticipo = request.POST.get("hasta_anticipo")
            search_anticipo = request.POST.get("search_anticipo")

            if calendario_general == False:
                leads_anticipo = Lead.objects.filter(etapa="Anticipo", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            else:
                leads_anticipo = Lead.objects.filter(etapa="Anticipo", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            
            if origen_lead_anticipo:
                leads_anticipo = leads_anticipo.filter(origen_lead=origen_lead_anticipo)
            if respuesta_anticipo:
                leads_anticipo = leads_anticipo.filter(respuesta=respuesta_anticipo)
            if estado_anticipo:
                leads_anticipo = leads_anticipo.filter(estado=estado_anticipo)
            if asesor_anticipo:
                leads_anticipo = leads_anticipo.filter(nombre_asesor=asesor_anticipo)
            if sala_anticipo:
                leads_anticipo = leads_anticipo.filter(sala=sala_anticipo)
            if desde_anticipo:
                desde_anticipo = datetime.strptime(desde_anticipo, '%Y-%m-%d').date()
                leads_anticipo = leads_anticipo.filter(fecha_apertura__gte=desde_anticipo)
            if hasta_anticipo:
                hasta_anticipo = datetime.strptime(hasta_anticipo, '%Y-%m-%d').date()
                leads_anticipo = leads_anticipo.filter(fecha_apertura__lte=hasta_anticipo)
            if search_anticipo:
                search_terms = search_anticipo.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_anticipo = leads_anticipo.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_anticipo = leads_anticipo.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_anticipo = leads_anticipo.filter(
                        Q(prospecto__nombre__icontains=search_anticipo) |
                        Q(prospecto__apellido_paterno__icontains=search_anticipo) |
                        Q(prospecto__apellido_materno__icontains=search_anticipo) |
                        Q(prospecto__celular__icontains=search_anticipo)
                    )

            if (leads_anticipo.count() % 15) == 0:
                cantidad_filtrado_pag = leads_anticipo.count() // 15
            else:
                cantidad_filtrado_pag = leads_anticipo.count() // 15 + 1

            leads_anticipo = leads_anticipo[page_min:page_max]
            
            leads_anticipo = list(leads_anticipo.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_anticipo.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_anticipo)
            return JsonResponse(leads_anticipo, safe=False)
    
        if request.POST.get("filtrar_conversion"):
            page_min = 0
            page_max = 15
            origen_lead_conversion = request.POST.get("origen_lead_conversion")
            respuesta_conversion = request.POST.get("respuesta_conversion")
            estado_conversion = request.POST.get("estado_conversion")
            asesor_conversion = request.POST.get("asesor_conversion")
            sala_conversion = request.POST.get("sala_conversion")
            marca_conversion = request.POST.get("marca_conversion")
            modelo_conversion = request.POST.get("modelo_conversion")
            desde_conversion = request.POST.get("desde_conversion")
            hasta_conversion = request.POST.get("hasta_conversion")
            search_conversion = request.POST.get("search_conversion")

            if calendario_general == False:
                leads_conversion = Lead.objects.filter(etapa="Conversión", activo=True, nombre_asesor=user.first_name).order_by("-fecha_apertura")
            else:
                leads_conversion = Lead.objects.filter(etapa="Conversión", activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")
            
            if origen_lead_conversion:
                leads_conversion = leads_conversion.filter(origen_lead=origen_lead_conversion)
            if respuesta_conversion:
                leads_conversion = leads_conversion.filter(respuesta=respuesta_conversion)
            if estado_conversion:
                leads_conversion = leads_conversion.filter(estado=estado_conversion)
            if asesor_conversion:
                leads_conversion = leads_conversion.filter(nombre_asesor=asesor_conversion)
            if sala_conversion:
                leads_conversion = leads_conversion.filter(sala=sala_conversion)
            if desde_conversion:
                desde_conversion = datetime.strptime(desde_conversion, '%Y-%m-%d').date()
                leads_conversion = leads_conversion.filter(fecha_apertura__gte=desde_conversion)
            if hasta_conversion:
                hasta_conversion = datetime.strptime(hasta_conversion, '%Y-%m-%d').date()
                leads_conversion = leads_conversion.filter(fecha_apertura__lte=hasta_conversion)
            if search_conversion:
                search_terms = search_conversion.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_conversion = leads_conversion.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_conversion = leads_conversion.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_conversion = leads_conversion.filter(
                        Q(prospecto__nombre__icontains=search_conversion) |
                        Q(prospecto__apellido_paterno__icontains=search_conversion) |
                        Q(prospecto__apellido_materno__icontains=search_conversion) |
                        Q(prospecto__celular__icontains=search_conversion)
                    )

            if (leads_conversion.count() % 15) == 0:
                cantidad_filtrado_pag = leads_conversion.count() // 15
            else:
                cantidad_filtrado_pag = leads_conversion.count() // 15 + 1

            leads_conversion = leads_conversion[page_min:page_max]
            
            leads_conversion = list(leads_conversion.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno",  "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_conversion.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_conversion)
            return JsonResponse(leads_conversion, safe=False)
    

class ReportesView(LoginRequiredMixin, TemplateView):
    # Vista de Reportes

    template_name = "Reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)

        leads = Lead.objects.filter(activo=True, nombre_asesor__isnull=False).order_by("-fecha_apertura")

        functions.verificar_primer_contacto_todos_los_leads(leads)

        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0
        print(user)

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads_no_contactado = Lead.objects.filter(activo=True, etapa="No contactado").order_by("-id")
        separados_y_facturados = VehiculosInteresLead.objects.filter(Q(separado=True) | Q(facturado=True)).values_list("lead").distinct()
        separados = VehiculosInteresLead.objects.filter(separado=True).values_list("lead").distinct()
        facturados = VehiculosInteresLead.objects.filter(facturado=True).values_list("lead").distinct()
        leads_facturados = Lead.objects.filter(activo=True, pk__in=facturados).order_by("-id")
        leads_separados = Lead.objects.filter(activo=True, pk__in=separados).order_by("-id")
        leads_separados_y_facturados = Lead.objects.filter(activo=True, pk__in=separados_y_facturados).order_by("-id")
        leads_desistidos = Lead.objects.filter(activo=True, etapa="Desistido").order_by("-id")
        leads_seguimiento = Lead.objects.filter(activo=True, etapa="Seguimiento").order_by("-id")
        leads_anticipo = Lead.objects.filter(activo=True, etapa="Anticipo").order_by("-id")

        print(leads_seguimiento)

        historial = Historial.objects.filter(lead__in=leads_no_contactado).values("lead").annotate(Max("fecha"))

        print("historial")
        print(historial)

        verificados = HistorialVerificaciones.objects.values("lead", "tipo_solicitud").distinct().order_by("-id")

        mostrado_marcas = VehiculosInteresLead.objects.filter(mostrado=True).values("lead").distinct().values("lead", "marca", "modelo", "codigo_vehiculo")
        separados_y_facturados_marcas = VehiculosInteresLead.objects.filter(mostrado=False).values("lead").distinct().values("lead", "marca", "modelo", "codigo_vehiculo", "fecha")

        origenes_lead_no_contactado = leads_no_contactado.order_by("origen_lead").values("origen_lead").distinct()
        
        respuestas_no_contactado = leads_no_contactado.order_by("respuesta").values("respuesta").distinct()
        respuestas_desistidos = leads_desistidos.order_by("respuesta").values("respuesta").distinct()
        respuestas_anticipo = leads_anticipo.order_by("respuesta").values("respuesta").distinct()
        
        estados_no_contactado = leads_no_contactado.order_by("estado").values("estado").distinct()
        estados_separados_y_facturados = leads_separados_y_facturados.order_by("estado").values("estado").distinct()
        estados_desistidos = leads_desistidos.order_by("estado").values("estado").distinct()
        estados_anticipo = leads_anticipo.order_by("estado").values("estado").distinct()

        anfitriones_no_contactado = leads_no_contactado.order_by("nombre_anfitrion").values("nombre_anfitrion").distinct()

        asesores_no_contactado = leads_no_contactado.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_separados_y_facturados = leads_separados_y_facturados.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_desistidos = leads_desistidos.order_by("nombre_asesor").values("nombre_asesor").distinct()
        asesores_anticipo = leads_anticipo.order_by("nombre_asesor").values("nombre_asesor").distinct()

        salas_no_contactado = leads_no_contactado.order_by("sala").values("sala").distinct()
        salas_separados_y_facturados = leads_separados_y_facturados.order_by("sala").values("sala").distinct()
        salas_desistidos = leads_desistidos.order_by("sala").values("sala").distinct()
        salas_anticipo = leads_anticipo.order_by("sala").values("sala").distinct()

        mostrado_marcas_no_contactado = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_no_contactado).values("lead", "mostrado").distinct().annotate(latest=Max("id")).values("lead", "marca", "modelo")
        mostrado_marcas_separados_y_facturados = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_separados_y_facturados).values("lead", "mostrado").distinct().annotate(latest=Max("id")).values("lead", "marca", "modelo")
        mostrado_marcas_desistidos = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_desistidos).values("lead", "mostrado").distinct().annotate(latest=Max("id")).values("lead", "marca", "modelo")
        mostrado_marcas_anticipo = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_anticipo).values("lead", "mostrado").distinct().annotate(latest=Max("id")).values("lead", "marca", "modelo")
       
        if (leads_no_contactado.count() % 15) == 0:
            cantidad_capturados_pag = leads_no_contactado.count() // 15
        else:
            cantidad_capturados_pag = leads_no_contactado.count() // 15 + 1
        if (leads_separados_y_facturados.count() % 15) == 0:
            cantidad_sep_y_fac_pag = leads_separados_y_facturados.count() // 15
        else:
            cantidad_sep_y_fac_pag = leads_separados_y_facturados.count() // 15 + 1
        if (leads_desistidos.count() % 15) == 0:
            cantidad_desistidos_pag = leads_desistidos.count() // 15
        else:
            cantidad_desistidos_pag = leads_desistidos.count() // 15 + 1
        if (leads_anticipo.count() % 15) == 0:
            cantidad_anticipo_pag = leads_anticipo.count() // 15
        else:
            cantidad_anticipo_pag = leads_anticipo.count() // 15 + 1

        context["anfitriones_no_contactado"] = anfitriones_no_contactado
        context["asesor_actual"] = asesor_actual
        context["asesores_no_contactado"] = asesores_no_contactado
        context["asesores_separados_y_facturados"] = asesores_separados_y_facturados
        context["asesores_desistidos"] = asesores_desistidos
        context["asesores_anticipo"] = asesores_anticipo
        context["calendario_general"] = calendario_general
        context["cantidad_no_contactado"] = leads_no_contactado.count()
        context["cantidad_capturados_pag"] = cantidad_capturados_pag
        context["cantidad_sep_y_fac_pag"] = cantidad_sep_y_fac_pag
        context["cantidad_desistidos_pag"] = cantidad_desistidos_pag
        context["cantidad_anticipo_pag"] = cantidad_anticipo_pag
        context["cantidad_seguimiento"] = leads_seguimiento.count()
        context["cantidad_desistidos"] = leads_desistidos.count()
        context["cantidad_anticipo"] = leads_anticipo.count()
        context["cantidad_historial"] = historial.count()
        context["cantidad_separados_y_facturados"] = leads_separados_y_facturados.count()
        context["estados_no_contactado"] = estados_no_contactado
        context["estados_separados_y_facturados"] = estados_separados_y_facturados
        context["estados_desistidos"] = estados_desistidos
        context["estados_anticipo"] = estados_anticipo
        context["historial"] = historial
        context["leads_no_contactado"] = leads_no_contactado[0:15]
        context["leads_seguimiento"] = leads_seguimiento[0:15]
        context["leads_desistidos"] = leads_desistidos[0:15]
        context["leads_facturados"] = leads_facturados[0:15]
        context["leads_separados"] = leads_separados[0:15]
        context["leads_separados_y_facturados"] = leads_separados_y_facturados[0:15]
        context["leads_anticipo"] = leads_anticipo[0:15]
        context["mostrado_marcas"] = mostrado_marcas
        context["mostrado_marcas_no_contactado"] = mostrado_marcas_no_contactado
        context["mostrado_marcas_separados_y_facturados"] = mostrado_marcas_separados_y_facturados
        context["mostrado_marcas_desistidos"] = mostrado_marcas_desistidos
        context["mostrado_marcas_anticipo"] = mostrado_marcas_anticipo
        context["pages_capturados"] = 1
        context["pages_sep_y_fac"] = 1
        context["pages_desistidos"] = 1
        context["origenes_lead_no_contactado"] = origenes_lead_no_contactado
        context["respuestas_no_contactado"] = respuestas_no_contactado
        context["respuestas_desistidos"] = respuestas_desistidos
        context["respuestas_anticipo"] = respuestas_anticipo
        context["salas_no_contactado"] = salas_no_contactado
        context["salas_separados_y_facturados"] = salas_separados_y_facturados
        context["salas_desistidos"] = salas_desistidos
        context["salas_anticipo"] = salas_anticipo
        context["separados"] = separados
        context["separados_y_facturados_marcas"] = separados_y_facturados_marcas
        context["user"] = user
        context["verificados"] = verificados

        return context
    
    def post(self, request):

        leads = Lead.objects.filter(activo=True, nombre_asesor__isnull=False).order_by("-id")

        origen_lead_capturados = request.POST.get("origen_lead_capturados")
        respuesta_capturados = request.POST.get("respuesta_capturados")
        estado_capturados = request.POST.get("estado_capturados")
        anfitrion_capturados = request.POST.get("anfitrion_capturados")
        asesor_capturados = request.POST.get("asesor_capturados")
        sala_capturados = request.POST.get("sala_capturados")
        verificado_capturados = request.POST.get("verificado_capturados")
        marca_capturados = request.POST.get("marca_capturados")
        modelo_capturados = request.POST.get("modelo_capturados")
        desde_capturados = request.POST.get("desde_capturados")
        hasta_capturados = request.POST.get("hasta_capturados")
        search_capturados = request.POST.get("search_capturados")

        try:
            json.loads(request.POST.get("if_filtrar_capturados"))
            if_filtrar_capturados = True
        except:
            if_filtrar_capturados = False


        if if_filtrar_capturados:
            if origen_lead_capturados:
                leads = leads.filter(origen_lead=origen_lead_capturados)
            if respuesta_capturados:
                leads = leads.filter(respuesta=respuesta_capturados)
            if estado_capturados:
                leads = leads.filter(estado=estado_capturados)
            if anfitrion_capturados:
                leads = leads.filter(nombre_asesor=anfitrion_capturados)
            if asesor_capturados:
                leads = leads.filter(nombre_asesor=asesor_capturados)
            if sala_capturados:
                leads = leads.filter(sala=sala_capturados)
            if verificado_capturados:
                if verificado_capturados == "SI":
                    leads = leads.filter(estado_llamada_verificacion__isnull=False)
                elif verificado_capturados == "NO":
                    leads = leads.filter(estado_llamada_verificacion__isnull=True)
            if desde_capturados:
                desde_capturados = datetime.strptime(desde_capturados, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_capturados)
            if hasta_capturados:
                hasta_capturados = datetime.strptime(hasta_capturados, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_capturados)
            if search_capturados:
                search_terms = search_capturados.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads = leads.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads = leads.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads = leads.filter(
                        Q(prospecto__nombre__icontains=search_capturados) |
                        Q(prospecto__apellido_paterno__icontains=search_capturados) |
                        Q(prospecto__apellido_materno__icontains=search_capturados) |
                        Q(prospecto__celular__icontains=search_capturados)
                    )

        respuesta_desistidos = request.POST.get("respuesta_desistidos")
        estado_desistidos = request.POST.get("estado_desistidos")
        asesor_desistidos = request.POST.get("asesor_desistidos")
        sala_desistidos = request.POST.get("sala_desistidos")
        marca_desistidos = request.POST.get("marca_desistidos")
        modelo_desistidos = request.POST.get("modelo_desistidos")
        desde_desistidos = request.POST.get("desde_desistidos")
        hasta_desistidos = request.POST.get("hasta_desistidos")
        search_desistidos = request.POST.get("search_desistidos")

        try:
            json.loads(request.POST.get("if_filtrar_desistidos"))
            if_filtrar_desistidos = True
        except:
            if_filtrar_desistidos = False


        if if_filtrar_desistidos:
            if respuesta_desistidos:
                leads = leads.filter(respuesta=respuesta_desistidos)
            if estado_desistidos:
                leads = leads.filter(estado=estado_desistidos)
            if asesor_desistidos:
                leads = leads.filter(nombre_asesor=asesor_desistidos)
            if sala_desistidos:
                leads = leads.filter(sala=sala_desistidos)
            if desde_desistidos:
                desde_desistidos = datetime.strptime(desde_desistidos, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_desistidos)
            if hasta_desistidos:
                hasta_desistidos = datetime.strptime(hasta_desistidos, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_desistidos)
            if search_desistidos:
                leads = leads.filter(prospecto__nombre__icontains=search_desistidos) | leads.filter(prospecto__celular__icontains=search_desistidos)

        respuesta_anticipo = request.POST.get("respuesta_anticipo")
        estado_anticipo = request.POST.get("estado_anticipo")
        asesor_anticipo = request.POST.get("asesor_anticipo")
        sala_anticipo = request.POST.get("sala_anticipo")
        desde_anticipo = request.POST.get("desde_anticipo")
        hasta_anticipo = request.POST.get("hasta_anticipo")
        search_anticipo = request.POST.get("search_anticipo")

        try:
            json.loads(request.POST.get("if_filtrar_anticipo"))
            if_filtrar_anticipo = True
        except:
            if_filtrar_anticipo = False

        if if_filtrar_anticipo:
            if respuesta_anticipo:
                leads = leads.filter(respuesta=respuesta_anticipo)
            if estado_anticipo:
                leads = leads.filter(estado=estado_anticipo)
            if asesor_anticipo:
                leads = leads.filter(nombre_asesor=asesor_anticipo)
            if sala_anticipo:
                leads = leads.filter(sala=sala_anticipo)
            if desde_anticipo:
                desde_anticipo = datetime.strptime(desde_anticipo, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__gte=desde_anticipo)
            if hasta_anticipo:
                hasta_anticipo = datetime.strptime(hasta_anticipo, '%Y-%m-%d').date()
                leads = leads.filter(fecha_apertura__lte=hasta_anticipo)
            if search_anticipo:
                leads = leads.filter(prospecto__nombre__icontains=search_anticipo) | leads.filter(prospecto__celular__icontains=search_anticipo)

        if request.POST.get("pages_capturados"):
            page_min = (int(request.POST.get("pages_capturados")) - 1) * 15
            page_max = int(request.POST.get("pages_capturados")) * 15
            leads_no_contactado = leads.filter(nombre_asesor__isnull=False, activo=True).order_by("-id")[page_min:page_max]
            leads_no_contactado = list(leads_no_contactado.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            print(page_min)
            print(page_max)
            print(leads_no_contactado)
            return JsonResponse(leads_no_contactado, safe=False)
        if request.POST.get("pages_sep_y_fac"):
            page_min = (int(request.POST.get("pages_sep_y_fac")) - 1) * 15
            page_max = int(request.POST.get("pages_sep_y_fac")) * 15
            separados_y_facturados = VehiculosInteresLead.objects.filter(Q(separado=True) | Q(facturado=True)).values_list("lead").distinct()
            leads_separados_y_facturados = leads.filter(pk__in=separados_y_facturados, activo=True).order_by("-id")[page_min:page_max]
            leads_separados_y_facturados = list(leads_separados_y_facturados.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            print(page_min)
            print(page_max)
            return JsonResponse(leads_separados_y_facturados, safe=False)
        if request.POST.get("pages_desistidos"):
            page_min = (int(request.POST.get("pages_desistidos")) - 1) * 15
            page_max = int(request.POST.get("pages_desistidos")) * 15
            leads_desistidos = leads.filter(etapa="Desistido", activo=True).order_by("-id")[page_min:page_max]
            leads_desistidos = list(leads_desistidos.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            print(page_min)
            print(page_max)
            return JsonResponse(leads_desistidos, safe=False)
        if request.POST.get("pages_anticipo"):
            page_min = (int(request.POST.get("pages_anticipo")) - 1) * 15
            page_max = int(request.POST.get("pages_anticipo")) * 15
            leads_anticipo = leads.filter(nombre_asesor__isnull=False, activo=True).order_by("-id")[page_min:page_max]
            leads_anticipo = list(leads_anticipo.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            print(page_min)
            print(page_max)
            return JsonResponse(leads_anticipo, safe=False)
        
        if request.POST.get("filtrar_capturados"):
            page_min = 0
            page_max = 15
            origen_lead_capturados = request.POST.get("origen_lead_capturados")
            respuesta_capturados = request.POST.get("respuesta_capturados")
            estado_capturados = request.POST.get("estado_capturados")
            anfitrion_capturados = request.POST.get("anfitrion_capturados")
            asesor_capturados = request.POST.get("asesor_capturados")
            sala_capturados = request.POST.get("sala_capturados")
            verificado_capturados = request.POST.get("verificado_capturados")
            marca_capturados = request.POST.get("marca_capturados")
            modelo_capturados = request.POST.get("modelo_capturados")
            desde_capturados = request.POST.get("desde_capturados")
            hasta_capturados = request.POST.get("hasta_capturados")
            search_capturados = request.POST.get("search_capturados")

            leads_capturados = Lead.objects.filter(nombre_asesor__isnull=False, activo=True).order_by("-id")
            
            if origen_lead_capturados:
                leads_capturados = leads_capturados.filter(origen_lead=origen_lead_capturados)
            if respuesta_capturados:
                leads_capturados = leads_capturados.filter(respuesta=respuesta_capturados)
            if estado_capturados:
                leads_capturados = leads_capturados.filter(estado=estado_capturados)
            if anfitrion_capturados:
                leads_capturados = leads_capturados.filter(nombre_anfitrion=anfitrion_capturados)
            if asesor_capturados:
                leads_capturados = leads_capturados.filter(nombre_asesor=asesor_capturados)
            if sala_capturados:
                leads_capturados = leads_capturados.filter(sala=sala_capturados)
            if verificado_capturados:
                if verificado_capturados == "SI":
                    leads_capturados = leads_capturados.filter(estado_llamada_verificacion__isnull=False)
                else:
                    leads_capturados = leads_capturados.filter(estado_llamada_verificacion__isnull=True)
            if desde_capturados:
                desde_capturados = datetime.strptime(desde_capturados, '%Y-%m-%d').date()
                leads_capturados = leads_capturados.filter(fecha_apertura__gte=desde_capturados)
            if hasta_capturados:
                hasta_capturados = datetime.strptime(hasta_capturados, '%Y-%m-%d').date()
                leads_capturados = leads_capturados.filter(fecha_apertura__lte=hasta_capturados)
            if search_capturados:
                search_terms = search_capturados.split()

                if len(search_terms) == 2:
                    term1, term2 = search_terms
                    leads_capturados = leads_capturados.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                        (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                    )
                elif len(search_terms) == 3:
                    term1, term2, term3 = search_terms
                    leads_capturados = leads_capturados.filter(
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                        (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                        (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                    )
                else:
                    # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                    leads_capturados = leads_capturados.filter(
                        Q(prospecto__nombre__icontains=search_capturados) |
                        Q(prospecto__apellido_paterno__icontains=search_capturados) |
                        Q(prospecto__apellido_materno__icontains=search_capturados) |
                        Q(prospecto__celular__icontains=search_capturados)
                    )

            if (leads_capturados.count() % 15) == 0:
                cantidad_filtrado_pag = leads_capturados.count() // 15
            else:
                cantidad_filtrado_pag = leads_capturados.count() // 15 + 1

            leads_capturados = leads_capturados[page_min:page_max]
            
            leads_capturados = list(leads_capturados.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_capturados.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_capturados)
            return JsonResponse(leads_capturados, safe=False)
        
        if request.POST.get("filtrar_desistidos"):
            page_min = 0
            page_max = 15
            origen_lead_desistidos = request.POST.get("origen_lead_desistidos")
            respuesta_desistidos = request.POST.get("respuesta_desistidos")
            estado_desistidos = request.POST.get("estado_desistidos")
            anfitrion_desistidos = request.POST.get("anfitrion_desistidos")
            asesor_desistidos = request.POST.get("asesor_desistidos")
            sala_desistidos = request.POST.get("sala_desistidos")
            verificado_desistidos = request.POST.get("verificado_desistidos")
            marca_desistidos = request.POST.get("marca_desistidos")
            modelo_desistidos = request.POST.get("modelo_desistidos")
            desde_desistidos = request.POST.get("desde_desistidos")
            hasta_desistidos = request.POST.get("hasta_desistidos")
            search_desistidos = request.POST.get("search_desistidos")

            leads_desistidos = Lead.objects.filter(etapa="Desistido", activo=True).order_by("-id")
            
            if origen_lead_desistidos:
                leads_desistidos = leads_desistidos.filter(origen_lead=origen_lead_desistidos)
            if respuesta_desistidos:
                leads_desistidos = leads_desistidos.filter(respuesta=respuesta_desistidos)
            if estado_desistidos:
                leads_desistidos = leads_desistidos.filter(estado=estado_desistidos)
            if anfitrion_desistidos:
                leads_desistidos = leads_desistidos.filter(nombre_anfitrion=anfitrion_desistidos)
            if asesor_desistidos:
                leads_desistidos = leads_desistidos.filter(nombre_asesor=asesor_desistidos)
            if sala_desistidos:
                leads_desistidos = leads_desistidos.filter(sala=sala_desistidos)
            if verificado_desistidos:
                if verificado_desistidos == "SI":
                    leads_desistidos = leads_desistidos.filter(estado_llamada_verificacion__isnull=False)
                else:
                    leads_desistidos = leads_desistidos.filter(estado_llamada_verificacion__isnull=True)
            if desde_desistidos:
                desde_desistidos = datetime.strptime(desde_desistidos, '%Y-%m-%d').date()
                leads_desistidos = leads_desistidos.filter(fecha_apertura__gte=desde_desistidos)
            if hasta_desistidos:
                hasta_desistidos = datetime.strptime(hasta_desistidos, '%Y-%m-%d').date()
                leads_desistidos = leads_desistidos.filter(fecha_apertura__lte=hasta_desistidos)
            if search_desistidos:
                leads_desistidos = leads_desistidos.filter(prospecto__nombre__icontains=search_desistidos) | leads_desistidos.filter(prospecto__celular__icontains=search_desistidos)


            if (leads_desistidos.count() % 15) == 0:
                cantidad_filtrado_pag = leads_desistidos.count() // 15
            else:
                cantidad_filtrado_pag = leads_desistidos.count() // 15 + 1

            leads_desistidos = leads_desistidos[page_min:page_max]
            
            leads_desistidos = list(leads_desistidos.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_desistidos.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_desistidos)
            return JsonResponse(leads_desistidos, safe=False)
    
        if request.POST.get("filtrar_anticipo"):
            page_min = 0
            page_max = 15
            respuesta_anticipo = request.POST.get("respuesta_anticipo")
            estado_anticipo = request.POST.get("estado_anticipo")
            asesor_anticipo = request.POST.get("asesor_anticipo")
            sala_anticipo = request.POST.get("sala_anticipo")
            desde_anticipo = request.POST.get("desde_anticipo")
            hasta_anticipo = request.POST.get("hasta_anticipo")
            search_anticipo = request.POST.get("search_anticipo")

            leads_anticipo = Lead.objects.filter(nombre_asesor__isnull=False, activo=True).order_by("-id")
            
            if respuesta_anticipo:
                leads_anticipo = leads_anticipo.filter(respuesta=respuesta_anticipo)
            if estado_anticipo:
                leads_anticipo = leads_anticipo.filter(estado=estado_anticipo)
            if asesor_anticipo:
                leads_anticipo = leads_anticipo.filter(nombre_asesor=asesor_anticipo)
            if sala_anticipo:
                leads_anticipo = leads_anticipo.filter(sala=sala_anticipo)
            if desde_anticipo:
                desde_anticipo = datetime.strptime(desde_anticipo, '%Y-%m-%d').date()
                leads_anticipo = leads_anticipo.filter(fecha_apertura__gte=desde_anticipo)
            if hasta_anticipo:
                hasta_anticipo = datetime.strptime(hasta_anticipo, '%Y-%m-%d').date()
                leads_anticipo = leads_anticipo.filter(fecha_apertura__lte=hasta_anticipo)
            if search_anticipo:
                leads_anticipo = leads_anticipo.filter(prospecto__nombre__icontains=search_anticipo) | leads_anticipo.filter(prospecto__celular__icontains=search_anticipo)

            if (leads_anticipo.count() % 15) == 0:
                cantidad_filtrado_pag = leads_anticipo.count() // 15
            else:
                cantidad_filtrado_pag = leads_anticipo.count() // 15 + 1

            leads_anticipo = leads_anticipo[page_min:page_max]
            
            leads_anticipo = list(leads_anticipo.values("id", "fecha_apertura", "prospecto__nombre", "prospecto__apellido_paterno", "prospecto__apellido_materno", "prospecto__celular", "prospecto__correo", "nombre_anfitrion", "tipo_documento", "documento", "campania", "respuesta", "estado", "origen_lead", "sala", "nombre_asesor", "estado_llamada_verificacion"))
            leads_anticipo.append(cantidad_filtrado_pag)
            print(page_min)
            print(page_max)
            print(leads_anticipo)
            return JsonResponse(leads_anticipo, safe=False)

class TiemposView(LoginRequiredMixin, TemplateView):
    # Vista de Tiempos

    template_name = "Tiempos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0
        print(user)

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads_tiempos = Lead.objects.filter(tiempo_primer_contacto__isnull=False, activo=True, fecha_hora_asignacion_asesor__isnull=False).annotate(dias_totales=(ExpressionWrapper((Cast(datetime.now(), output_field=DateTimeField())) - F('fecha_hora_asignacion_asesor'), output_field=IntegerField()))).order_by("-id")
        
        leads_verificados = Lead.objects.filter(estado_llamada_verificacion__isnull=False, activo=True).order_by("-id")

        verificados = HistorialVerificaciones.objects.values("lead", "tipo_solicitud").distinct().order_by("-id")

        mostrado_marcas = VehiculosInteresLead.objects.filter(mostrado=True).values("lead").distinct().values("lead", "marca", "modelo")

        origenes_lead_tiempos = leads_tiempos.order_by("origen_lead").values("origen_lead").distinct()
        respuestas_tiempos = leads_tiempos.order_by("respuesta").values("respuesta").distinct()
        estados_tiempos = leads_tiempos.order_by("estado").values("estado").distinct()
        asesores_tiempos = leads_tiempos.order_by("nombre_asesor").values("nombre_asesor").distinct()
        salas_tiempos = leads_tiempos.order_by("sala").values("sala").distinct()
        marcas_tiempos = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_tiempos).values("marca").distinct()
        modelos_tiempos = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_tiempos).values("modelo").distinct() 

        context["asesor_actual"] = asesor_actual
        context["asesores_tiempos"] = asesores_tiempos
        context["calendario_general"] = calendario_general
        context["cantidad_tiempos"] = leads_tiempos.count()
        context["cantidad_verificados"] = leads_verificados.count()
        context["estados_tiempos"] = estados_tiempos
        context["leads_tiempos"] = leads_tiempos[0:15]
        context["leads_verificados"] = leads_verificados
        context["marcas_tiempos"] = marcas_tiempos
        context["modelos_tiempos"] = modelos_tiempos
        context["mostrado_marcas"] = mostrado_marcas
        context["origenes_lead_tiempos"] = origenes_lead_tiempos
        context["respuestas_tiempos"] = respuestas_tiempos
        context["salas_tiempos"] = salas_tiempos
        context["user"] = user
        context["verificados"] = verificados

        return context
        
class AnuladosView(LoginRequiredMixin, TemplateView):
    # Vista de Anulados

    template_name = "Anulados.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads_anulados = Lead.objects.filter(activo=False).order_by("-id")
        leads_verificados = Lead.objects.filter(estado_llamada_verificacion__isnull=False).order_by("-id")

        verificados = HistorialVerificaciones.objects.values("lead", "tipo_solicitud").distinct().order_by("-id")

        mostrado_marcas = VehiculosInteresLead.objects.filter(mostrado=True).values("lead").distinct().values("lead", "marca", "modelo")

        origenes_lead_anulados = leads_anulados.order_by("origen_lead").values("origen_lead").distinct()
        respuestas_anulados = leads_anulados.order_by("respuesta").values("respuesta").distinct()
        estados_anulados = leads_anulados.order_by("estado").values("estado").distinct()
        asesores_anulados = leads_anulados.order_by("nombre_asesor").values("nombre_asesor").distinct()
        salas_anulados = leads_anulados.order_by("sala").values("sala").distinct()
        marcas_anulados = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_anulados).values("marca").distinct()
        modelos_anulados = VehiculosInteresLead.objects.filter(mostrado=True).filter(lead__in=leads_anulados).values("modelo").distinct() 

        origen_lead_anulados = self.request.GET.get("origen_lead_anulados") if self.request.GET.get("origen_lead_anulados") != "None" else None
        respuesta_anulados = self.request.GET.get("respuesta_anulados") if self.request.GET.get("respuesta_anulados") != "None" else None
        estado_anulados = self.request.GET.get("estado_anulados") if self.request.GET.get("estado_anulados") != "None" else None
        asesor_anulados = self.request.GET.get("asesor_anulados") if self.request.GET.get("asesor_anulados") != "None" else None
        sala_anulados = self.request.GET.get("sala_anulados") if self.request.GET.get("sala_anulados") != "None" else None
        desde_anulados = self.request.GET.get("desde_anulados") if self.request.GET.get("desde_anulados") != "None" else None
        hasta_anulados = self.request.GET.get("hasta_anulados") if self.request.GET.get("hasta_anulados") != "None" else None
        search_anulados = self.request.GET.get("search_anulados") if self.request.GET.get("search_anulados") != "None" else None

        if origen_lead_anulados:
            leads_anulados = leads_anulados.filter(origen_lead=origen_lead_anulados)
        if respuesta_anulados:
            leads_anulados = leads_anulados.filter(respuesta=respuesta_anulados)
        if estado_anulados:
            leads_anulados = leads_anulados.filter(estado=estado_anulados)
        if asesor_anulados:
            leads_anulados = leads_anulados.filter(nombre_asesor=asesor_anulados)
        if sala_anulados:
            leads_anulados = leads_anulados.filter(sala=sala_anulados)
        if desde_anulados:
            desde_anulados = datetime.strptime(desde_anulados, '%Y-%m-%d').date()
            leads_anulados = leads_anulados.filter(fecha_apertura__gte=desde_anulados)
        if hasta_anulados:
            hasta_anulados = datetime.strptime(hasta_anulados, '%Y-%m-%d').date()
            leads_anulados = leads_anulados.filter(fecha_apertura__lte=hasta_anulados)
        if search_anulados:
            search_terms = search_anulados.split()

            if len(search_terms) == 2:
                term1, term2 = search_terms
                leads_anulados = leads_anulados.filter(
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                    (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                )
            elif len(search_terms) == 3:
                term1, term2, term3 = search_terms
                leads_anulados = leads_anulados.filter(
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                )
            else:
                # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                leads_anulados = leads_anulados.filter(
                    Q(prospecto__nombre__icontains=search_anulados) |
                    Q(prospecto__apellido_paterno__icontains=search_anulados) |
                    Q(prospecto__apellido_materno__icontains=search_anulados) |
                    Q(prospecto__celular__icontains=search_anulados)
                )

        page = self.request.GET.get("page")
        paginator = Paginator(leads_anulados, self.paginate_by)
        page_obj = paginator.get_page(page)

        print("user")
        print(user)

        context["asesor_actual"] = asesor_actual
        context["asesores_anulados"] = asesores_anulados
        context["calendario_general"] = calendario_general
        context["cantidad_anulados"] = leads_anulados.count()
        context["cantidad_verificados"] = leads_verificados.count()
        context["estados_anulados"] = estados_anulados
        context["leads_anulados"] = page_obj
        context["leads_verificados"] = leads_verificados
        context["marcas_anulados"] = marcas_anulados
        context["modelos_anulados"] = modelos_anulados
        context["mostrado_marcas"] = mostrado_marcas
        context["origenes_lead_anulados"] = origenes_lead_anulados
        context["respuestas_anulados"] = respuestas_anulados
        context["salas_anulados"] = salas_anulados
        context["user"] = user
        context["group"] = user.groups.get()
        context["verificados"] = verificados

        context["has_previous"] = page_obj.has_previous()
        context["has_next"] = page_obj.has_next()
        context["has_other_pages"] = paginator.num_pages > 1
        context["page_number"] = page_obj.number
        context["page_max"] = paginator.num_pages
        context["previous_page_number"] = page_obj.previous_page_number
        context["next_page_number"] = page_obj.next_page_number
        context["paginator"] = paginator

        context["origen_lead_anulados"] = origen_lead_anulados
        context["respuesta_anulados"] = respuesta_anulados
        context["estado_anulados"] = estado_anulados
        context["asesor_anulados"] = asesor_anulados
        context["sala_anulados"] = sala_anulados
        context["desde_anulados"] = desde_anulados
        context["hasta_anulados"] = hasta_anulados
        context["search_anulados"] = search_anulados
        return context
    
    def post(self, request):

        leads_anulados = Lead.objects.filter(activo=False).values_list(
            "id",
            "fecha_apertura",
            "prospecto__nombre",
            "prospecto__celular",
            "origen_lead",
            "respuesta",
            "estado",
            "sala",
            "nombre_asesor",
            "prospecto__apellido_paterno",
            "prospecto__apellido_materno",
        ).order_by("-id")

        content_type = self.request.POST.get("content_type") if self.request.POST.get("content_type") != "None" else None
        origen_lead_anulados = self.request.POST.get("origen_lead_anulados") if self.request.POST.get("origen_lead_anulados") != "None" else None
        respuesta_anulados = self.request.POST.get("respuesta_anulados") if self.request.POST.get("respuesta_anulados") != "None" else None
        estado_anulados = self.request.POST.get("estado_anulados") if self.request.POST.get("estado_anulados") != "None" else None
        asesor_anulados = self.request.POST.get("asesor_anulados") if self.request.POST.get("asesor_anulados") != "None" else None
        sala_anulados = self.request.POST.get("sala_anulados") if self.request.POST.get("sala_anulados") != "None" else None
        desde_anulados = self.request.POST.get("desde_anulados") if self.request.POST.get("desde_anulados") != "None" else None
        hasta_anulados = self.request.POST.get("hasta_anulados") if self.request.POST.get("hasta_anulados") != "None" else None
        search_anulados = self.request.POST.get("search_anulados") if self.request.POST.get("search_anulados") != "None" else None

        if origen_lead_anulados:
            leads_anulados = leads_anulados.filter(origen_lead=origen_lead_anulados)
        if respuesta_anulados:
            leads_anulados = leads_anulados.filter(respuesta=respuesta_anulados)
        if estado_anulados:
            leads_anulados = leads_anulados.filter(estado=estado_anulados)
        if asesor_anulados:
            leads_anulados = leads_anulados.filter(nombre_asesor=asesor_anulados)
        if sala_anulados:
            leads_anulados = leads_anulados.filter(sala=sala_anulados)
        if desde_anulados:
            desde_anulados = datetime.strptime(desde_anulados, '%Y-%m-%d').date()
            leads_anulados = leads_anulados.filter(fecha_apertura__gte=desde_anulados)
        if hasta_anulados:
            hasta_anulados = datetime.strptime(hasta_anulados, '%Y-%m-%d').date()
            leads_anulados = leads_anulados.filter(fecha_apertura__lte=hasta_anulados)
        if search_anulados:
            search_terms = search_anulados.split()

            if len(search_terms) == 2:
                term1, term2 = search_terms
                leads_anulados = leads_anulados.filter(
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2)) |
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__nombre__icontains=term2)) |
                    (Q(prospecto__apellido_materno__icontains=term1) & Q(prospecto__nombre__icontains=term2))
                )
            elif len(search_terms) == 3:
                term1, term2, term3 = search_terms
                leads_anulados = leads_anulados.filter(
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term2) & Q(prospecto__apellido_materno__icontains=term3)) |
                    (Q(prospecto__nombre__icontains=term1) & Q(prospecto__apellido_paterno__icontains=term3) & Q(prospecto__apellido_materno__icontains=term2)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term2) & Q(prospecto__nombre__icontains=term3)) |
                    (Q(prospecto__apellido_paterno__icontains=term1) & Q(prospecto__apellido_materno__icontains=term3) & Q(prospecto__nombre__icontains=term2))
                )
            else:
                # Si hay solo un término, o más de 3 términos, busca en todos los campos relevantes.
                leads_anulados = leads_anulados.filter(
                    Q(prospecto__nombre__icontains=search_anulados) |
                    Q(prospecto__apellido_paterno__icontains=search_anulados) |
                    Q(prospecto__apellido_materno__icontains=search_anulados) |
                    Q(prospecto__celular__icontains=search_anulados)
                )

        if content_type == "excel":
            response = HttpResponse(content_type='application/ms-excel')

            #decide file name
            response['Content-Disposition'] = 'attachment; filename="Leads_Anulados.xls"'

            #creating workbook
            wb = xlwt.Workbook(encoding='utf-8')

            #adding sheet
            ws = wb.add_sheet("sheet1")

            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            # headers are bold
            font_style.font.bold = True

            #column header names, you can use your own headers here
            columns = ['Detalle', 'Fecha de Ingreso', 'Cliente', 'Telefono', 'Marca', 'Modelo', 'Origen de Ingreso', 'Respuesta Cliente', 'Estado', 'Sala', 'Asesor']

            # Escribe los encabezados de columna en la hoja
            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title, font_style)

            # Fuente sin bold
            font_style = xlwt.XFStyle()

            # Itera sobre los datos obtenidos y escribe en el archivo Excel
            for row in leads_anulados:
                row_num += 1
                # Escribe cada campo en la fila correspondiente
                ws.write(row_num, 0, "Detalle", font_style)  # Detalle
                ws.write(row_num, 1, str(row[1]) or "", font_style)  # Fecha de Ingreso
                ws.write(row_num, 2, f"{str(row[2])} {str(row[9])} {str(row[10])}" or "" or "", font_style)  # Cliente
                ws.write(row_num, 3, row[3] or "", font_style)  # Telefono
                ws.write(row_num, 4, "", font_style)  # Marca (vacío)
                ws.write(row_num, 5, "", font_style)  # Modelo (vacío)
                ws.write(row_num, 6, row[4] or "", font_style)  # Origen de Ingreso
                ws.write(row_num, 7, row[5] or "", font_style)  # Respuesta Cliente
                ws.write(row_num, 8, row[6] or "", font_style)  # Estado
                ws.write(row_num, 9, row[7] or "", font_style)  # Sala
                ws.write(row_num, 10, row[8] or "", font_style)  # Asesor

            wb.save(response)

        elif content_type == "csv":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Leads_Anulados.csv"'

            writer = csv.writer(response)
            # Escribe los encabezados de las columnas
            writer.writerow(['Detalle', 'Fecha de Ingreso', 'Cliente', 'Telefono', 'Marca', 'Modelo', 'Origen de Ingreso', 'Respuesta Cliente', 'Estado', 'Sala', 'Asesor'])

            # Escribe los datos
            for row in leads_anulados:
                writer.writerow([
                    "Detalle",  # Ajusta este campo según sea necesario
                    str(row[1]) or "",
                    f"{str(row[2])} {str(row[9])} {str(row[10])}" or "",
                    row[3] or "",
                    "",  # Ajusta este campo según sea necesario
                    "",  # Ajusta este campo según sea necesario
                    row[4] or "",
                    row[5] or "",
                    row[6] or "",
                    row[7] or "",
                    row[8] or ""
                ])

        return response

class ModernizeView(LoginRequiredMixin, TemplateView):
    # Vista de Modernize

    template_name = "Modernize.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        print(user)

        context["user"] = user

        return context
    
class Modernize2View(LoginRequiredMixin, TemplateView):
    # Vista de Modernize2

    template_name = "Modernize2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        print(user)

        context["user"] = user

        return context
    
class ReportesEventosView(LoginRequiredMixin, TemplateView):
    # Vista de Reportes Eventos

    template_name = "ReportesEventos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)

        leads = Lead.objects.filter(nombre_asesor__isnull=False).order_by("-id")

        functions.verificar_primer_contacto_todos_los_leads(leads)

        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0
        print(user)
        
        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        leads_activos = Lead.objects.filter(nombre_asesor__isnull=False).exclude(etapa="Desistido").exclude(respuesta="Entrega Finalizada")
        asesores = Asesor.objects.all()
        asesores_ecatepec = Asesor.objects.filter(sala="Xalostoc Ecatepec")
        today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
        today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
        cantidad_hoy = Evento.objects.filter(fecha_hora__range=(today_min, today_max)).count()
        eventos_hoy = Evento.objects.filter(fecha_hora__range=(today_min, today_max)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_pendientes = Evento.objects.filter(fecha_hora__gt=timezone.now(), cumplido=False).count()
        eventos_pendientes = Evento.objects.filter(fecha_hora__gt=today_max).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_cumplidos = Evento.objects.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).count()
        eventos_cumplidos = Evento.objects.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        eventos_vencidos = Evento.objects.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_vencidos = Evento.objects.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).count()
        list_sin_eventos = Evento.objects.all().values("lead").distinct()
        leads_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).values("nombre_asesor").annotate(cantidad=Count("pk"))
        cantidad_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).count()

        print("leads_sin_eventos")
        print(leads_sin_eventos)

        context["asesor_actual"] = asesor_actual
        context["asesores"] = asesores
        context["asesores_ecatepec"] = asesores_ecatepec
        context["calendario_general"] = calendario_general
        context["cantidad_activos"] = leads_activos.count()
        context["cantidad_cumplidos"] = cantidad_cumplidos
        context["cantidad_hoy"] = cantidad_hoy
        context["cantidad_pendientes"] = cantidad_pendientes
        context["cantidad_vencidos"] = cantidad_vencidos
        context["cantidad_sin_eventos"] = cantidad_sin_eventos
        context["eventos_cumplidos"] = eventos_cumplidos
        context["eventos_hoy"] = eventos_hoy
        context["eventos_pendientes"] = eventos_pendientes
        context["eventos_vencidos"] = eventos_vencidos
        context["leads_activos"] = leads_activos
        context["leads_sin_eventos"] = leads_sin_eventos
        context["user"] = user

        return context
    
    def post(self, request):

        user = User.objects.get(username=self.request.user)

        asesores = Asesor.objects.all()
        sala = request.POST.get("sala")
        desde = request.POST.get("desde")
        hasta = request.POST.get("hasta")

        try:
            json.loads(request.POST.get("if_filtrar_capturados"))
            if_filtrar_capturados = True
        except:
            if_filtrar_capturados = False

        if request.POST.get("filtrar_capturados"):
            asesores = Asesor.objects.all()
            if sala:
                asesores = asesores.filter(sala=sala)
            if desde:
                desde = datetime.strptime(desde, '%Y-%m-%d')
                eventos = list(Evento.objects.filter(fecha_hora__gte=desde).values_list("asesor", flat=True))
                asesores = asesores.filter(id__in=eventos)
            if hasta:
                hasta = datetime.strptime(hasta, '%Y-%m-%d')
                eventos = list(Evento.objects.filter(fecha_hora__lte=hasta).values_list("asesor", flat=True))
                asesores = asesores.filter(id__in=eventos)
            asesores = list(asesores.values("nombre"))
            return JsonResponse(asesores, safe=False)

        if request.POST.get("EventoNombre"):

            nombre = request.POST.get("EventoNombre")
            tipo = request.POST.get("EventoTipo")
            telefono_cliente = request.POST.get("EventoTelefono")
            observaciones = request.POST.get("EventoObservaciones")
            asesor = request.POST.get("EventoAsesor")
            fecha_hora = request.POST.get("EventoFechaHora")
            
            prospecto = Prospecto.objects.get(celular=telefono_cliente)
            cliente = prospecto.nombre + " " + prospecto.apellido_paterno + " " + prospecto.apellido_materno

            evento = Evento.objects.create(nombre=nombre,
                                           tipo=tipo,
                                           cliente=cliente,
                                           telefono_cliente=telefono_cliente,
                                           observaciones=observaciones,
                                           asesor=Asesor.objects.get(nombre=asesor),
                                           fecha_hora=datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M"),
                                           lead=Lead.objects.get(id=21)
                                           )
            return JsonResponse(evento.pk, safe=False)

class CalendarView(LoginRequiredMixin, TemplateView):
    # Vista de Calendar

    template_name = "Calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0
            asesor_actual["nombre"] = ""

        admin_group = Group.objects.filter(name__in=[
                'Admin',
            ])
        if user.groups.filter(pk__in=admin_group.values_list('pk', flat=True)).exists():
            is_admin = True
        else:
            is_admin = False

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        asesores = Asesor.objects.all()

        eventos = Evento.objects.all()

        today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
        today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
        cantidad_cumplidos = Evento.objects.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).count()
        eventos_cumplidos = Evento.objects.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_hoy = Evento.objects.filter(fecha_hora__range=(today_min, today_max)).count()
        eventos_hoy = Evento.objects.filter(fecha_hora__range=(today_min, today_max)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_pendientes = Evento.objects.filter(fecha_hora__gt=timezone.now(), cumplido=False).count()
        eventos_pendientes = Evento.objects.filter(fecha_hora__gt=today_max).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_vencidos = Evento.objects.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).count()
        eventos_vencidos = Evento.objects.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        leads_activos = Lead.objects.filter(nombre_asesor__isnull=False).exclude(etapa="Desistido").exclude(respuesta="Entrega Finalizada")
        list_sin_eventos = Evento.objects.all().values("lead").distinct()
        leads_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).values("nombre_asesor").annotate(cantidad=Count("pk"))
        cantidad_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).count()


        etapas = CatalogoRespuestasByEtapa.objects.values("etapa").distinct()
        respuestas = CatalogoRespuestasByEtapa.objects.values("respuesta").distinct()

        general = True

        prospectos = Lead.objects.exclude(etapa="Desistido").exclude(respuesta="Entrega Finalizada").distinct()

        print("is_admin")
        print(is_admin)

        context["asesor_actual"] = asesor_actual
        context["asesores"] = asesores
        context["calendario_general"] = calendario_general
        context["cantidad_cumplidos"] = cantidad_cumplidos
        context["cantidad_hoy"] = cantidad_hoy
        context["cantidad_pendientes"] = cantidad_pendientes
        context["cantidad_sin_eventos"] = cantidad_sin_eventos
        context["cantidad_vencidos"] = cantidad_vencidos
        context["etapas"] = etapas
        context["eventos"] = eventos
        context["eventos_cumplidos"] = eventos_cumplidos
        context["eventos_hoy"] = eventos_hoy
        context["eventos_pendientes"] = eventos_pendientes
        context["eventos_vencidos"] = eventos_vencidos
        context["general"] = general
        context["leads_sin_eventos"] = leads_sin_eventos
        context["prospectos"] = prospectos
        context["respuestas"] = respuestas
        context["user"] = user
        context["is_admin"] = is_admin

        return context

    def post(self, request):
        r = request.POST
        user = User.objects.get(username=self.request.user)
        
        print(r)
        if r.get("nombre_evento", None):
            nombre = r.get("nombre_evento", None)
            tipo = r.get("tipo", None)
            telefono_cliente = r.get("telefono_cliente", None)
            observaciones = r.get("observaciones", None)
            asesor = r.get("asesor", None)
            fecha_hora = r.get("fecha_hora", None)
            tiempo = r.get("tiempo", None)

            prospecto = Prospecto.objects.get(celular=telefono_cliente)
            cliente = prospecto.nombre + " " + prospecto.apellido_paterno + " " + prospecto.apellido_materno

            lead = Lead.objects.get(prospecto__celular=telefono_cliente)
            evento = Evento.objects.create(nombre=nombre,
                                           tipo=tipo,
                                           cliente=cliente,
                                           telefono_cliente=telefono_cliente,
                                           observaciones=observaciones,
                                           asesor=Asesor.objects.get(nombre=asesor),
                                           fecha_hora=datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M"),
                                           lead=lead,
                                           tiempo_evento=tiempo
                                           )

            Historial.objects.create(lead=lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se creó un evento. Nombre: {nombre}. Tipo: {tipo}. Observaciones: {observaciones}",
                                    )

            return HttpResponseRedirect(reverse_lazy('dashboards:calendar'))

        if r.get("id_evento", None):
            id = r.get("id_evento", None)
            evento = Evento.objects.get(id=id)

            Historial.objects.create(lead=evento.lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se eliminó un evento. Nombre: {evento.nombre}. Tipo: {evento.tipo}. Observaciones: {evento.observaciones}",
                                    )
            evento.delete()

            

            return HttpResponseRedirect(reverse_lazy('dashboards:calendar'))
        if r.get("id_evento2", None):
            id = r.get("id_evento2", None)
            evento = Evento.objects.get(id=id).lead.pk
            
            print(evento)

            return JsonResponse(evento, safe=False)
        if r.get("id_evento_cumplido", None):
            id = r.get("id_evento_cumplido", None)
            evento = Evento.objects.get(id=id)
            evento.cumplido = True
            evento.fecha_hora_cumplido = datetime.now()
            evento.save()

            Historial.objects.create(lead=evento.lead,
                        fecha=date.today(),
                        hora=datetime.now().time(),
                        responsable=user,
                        operacion=f"Se cumplió un evento. Nombre: {evento.nombre}. Tipo: {evento.tipo}. Observaciones: {evento.observaciones}",
                        )
            
            return HttpResponseRedirect(reverse_lazy('dashboards:calendar'))
        if r.get("EventoNombre"):

            id = request.POST.get("EventoId")
            nombre = request.POST.get("EventoNombre")
            tipo = request.POST.get("EventoTipo")
            observaciones = request.POST.get("EventoObservaciones")
            asesor = request.POST.get("EventoAsesor")
            fecha_hora = request.POST.get("EventoFechaHora")

            print("fecha_hora")
            print(type(fecha_hora))

            print(date.today())
            print(type(date.today()))

            print(datetime.now().time())
            print(type(datetime.now().time()))

            evento = Evento.objects.get(id=id)
            evento.nombre=nombre
            evento.tipo=tipo
            evento.observaciones=observaciones
            evento.asesor=Asesor.objects.get(nombre=asesor)
            evento.fecha_hora=make_aware(datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M"))
            evento.save()
            Historial.objects.create(lead=evento.lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se editó un evento. Nombre: {nombre}. Tipo: {tipo}. Observaciones: {observaciones}",
                                    )
            return JsonResponse(evento.pk, safe=False)

class CalendarDetailView(LoginRequiredMixin, DetailView):
    # Vista de Calendar Detail

    template_name = "Calendar.html"
    slug_field = "adviser"
    slug_url_kwarg = "adviser"
    queryset = Asesor.objects.all()
    context_object_name = "adviser"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adviser = self.get_object()
        user = User.objects.get(username=self.request.user)
        try:
            asesor_actual = Asesor.objects.get(nombre=user.first_name)
        except:
            asesor_actual = {}
            asesor_actual["pk"] = 0

        calendario_general = True
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                calendario_general = False

        asesores = Asesor.objects.all()

        eventos = Evento.objects.filter(asesor=adviser)

        today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
        today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
        cantidad_cumplidos = eventos.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).count()
        eventos_cumplidos = eventos.filter(cumplido=True, fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_hoy = eventos.filter(fecha_hora__range=(today_min, today_max)).count()
        eventos_hoy = eventos.filter(fecha_hora__range=(today_min, today_max)).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_pendientes = eventos.filter(fecha_hora__gt=timezone.now(), cumplido=False).count()
        eventos_pendientes = eventos.filter(fecha_hora__gt=today_max).values("asesor").annotate(cantidad=Count("pk"))
        cantidad_vencidos = eventos.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).count()
        eventos_vencidos = eventos.filter(cumplido=False, fecha_hora__date__lte=timezone.now(), fecha_hora__date__gte=date.today()-timedelta(30)).values("asesor").annotate(cantidad=Count("pk"))
        leads_activos = Lead.objects.filter(nombre_asesor=adviser.nombre).exclude(etapa="Desistido").exclude(respuesta="Entrega Finalizada")
        list_sin_eventos = eventos.values("lead").distinct()
        leads_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).values("nombre_asesor").annotate(cantidad=Count("pk"))
        cantidad_sin_eventos = leads_activos.exclude(id__in=list_sin_eventos).count()
        
        etapas = CatalogoRespuestasByEtapa.objects.values("etapa").distinct()
        respuestas = CatalogoRespuestasByEtapa.objects.values("respuesta").distinct()

        print(user)
        print(adviser.pk)

        mostrar_evento = False
        for grupo in self.request.user.groups.all():
            if grupo.name == "Asesor":
                mostrar_evento = True

        general = False

        prospectos = Lead.objects.exclude(etapa="Desistido").exclude(respuesta="Entrega Finalizada").filter(nombre_asesor=user.first_name).distinct()

        print(prospectos)

        context["adviser"] = adviser
        context["asesor_actual"] = asesor_actual
        context["asesores"] = asesores
        context["calendario_general"] = calendario_general
        context["cantidad_cumplidos"] = cantidad_cumplidos
        context["cantidad_hoy"] = cantidad_hoy
        context["cantidad_pendientes"] = cantidad_pendientes
        context["cantidad_vencidos"] = cantidad_vencidos
        context["cantidad_sin_eventos"] = cantidad_sin_eventos
        context["etapas"] = etapas
        context["eventos"] = eventos
        context["eventos_cumplidos"] = eventos_cumplidos
        context["eventos_hoy"] = eventos_hoy
        context["eventos_pendientes"] = eventos_pendientes
        context["eventos_vencidos"] = eventos_vencidos
        context["general"] = general
        context["leads_sin_eventos"] = leads_sin_eventos
        context["mostrar_evento"] = mostrar_evento
        context["prospectos"] = prospectos
        context["respuestas"] = respuestas
        context["user"] = user

        return context

    def post(self, request, pk):
        r = request.POST
        adviser = self.get_object()
        user = User.objects.get(username=self.request.user)
        
        print(r)
        if r.get("nombre_evento", None):
            nombre = r.get("nombre_evento", None)
            tipo = r.get("tipo", None)
            telefono_cliente = r.get("telefono_cliente", None)
            observaciones = r.get("observaciones", None)
            asesor = r.get("asesor", None)
            fecha_hora = r.get("fecha_hora", None)
            tiempo = r.get("tiempo", None)

            prospecto = Prospecto.objects.get(celular=telefono_cliente)
            cliente = prospecto.nombre + " " + prospecto.apellido_paterno + " " + prospecto.apellido_materno
            
            print(telefono_cliente)
            print(asesor)
            print(type(telefono_cliente))

            lead = Lead.objects.get(prospecto__celular=telefono_cliente)
            evento = Evento.objects.create(nombre=nombre,
                                           tipo=tipo,
                                           cliente=cliente,
                                           telefono_cliente=telefono_cliente,
                                           observaciones=observaciones,
                                           asesor=Asesor.objects.get(nombre=asesor),
                                           fecha_hora=datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M"),
                                           lead=lead,
                                           tiempo_evento=tiempo
                                           )

            Historial.objects.create(lead=lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se creó un evento. Nombre: {nombre}. Tipo: {tipo}. Observaciones: {observaciones}",
                                    )

            return HttpResponseRedirect(reverse_lazy('dashboards:calendar_detail', kwargs={"pk": pk}))
        if r.get("id_evento", None):
            id = r.get("id_evento", None)
            evento = Evento.objects.get(id=id)

            Historial.objects.create(lead=evento.lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se eliminó un evento. Nombre: {evento.nombre}. Tipo: {evento.tipo}. Observaciones: {evento.observaciones}",
                                    )
            evento.delete()

            return HttpResponseRedirect(reverse_lazy('dashboards:calendar'))
        if r.get("id_evento2", None):
            id = r.get("id_evento2", None)
            telefono = r.get("telefono", None)
            try:
                Lead.objects.get(prospecto__celular=telefono, nombre_asesor=adviser.nombre)
                evento = Evento.objects.get(id=id).lead.pk
            
                return JsonResponse(evento, safe=False)
            except:
                pass  
        if r.get("id_evento_cumplido", None):
            id = r.get("id_evento_cumplido", None)
            evento = Evento.objects.get(id=id)
            evento.cumplido = True
            evento.fecha_hora_cumplido = datetime.now()
            evento.save()

            Historial.objects.create(lead=evento.lead,
                        fecha=date.today(),
                        hora=datetime.now().time(),
                        responsable=user,
                        operacion=f"Se cumplió un evento. Nombre: {evento.nombre}. Tipo: {evento.tipo}. Observaciones: {evento.observaciones}",
                        )
            
            return HttpResponseRedirect(reverse_lazy('dashboards:calendar_detail', kwargs={"pk": pk}))
        if r.get("EventoNombre"):
            id = request.POST.get("EventoId")
            nombre = request.POST.get("EventoNombre")
            tipo = request.POST.get("EventoTipo")
            observaciones = request.POST.get("EventoObservaciones")
            asesor = request.POST.get("EventoAsesor")
            fecha_hora = request.POST.get("EventoFechaHora")

            print("fecha_hora")
            print(type(fecha_hora))

            print(date.today())
            print(type(date.today()))

            print(datetime.now().time())
            print(type(datetime.now().time()))

            evento = Evento.objects.get(id=id)
            evento.nombre=nombre
            evento.tipo=tipo
            evento.observaciones=observaciones
            evento.asesor=Asesor.objects.get(nombre=asesor)
            evento.fecha_hora=make_aware(datetime.strptime(fecha_hora,"%Y-%m-%dT%H:%M"))
            evento.save()
            Historial.objects.create(lead=evento.lead,
                                    fecha=date.today(),
                                    hora=datetime.now().time(),
                                    responsable=user,
                                    operacion=f"Se editó un evento. Nombre: {nombre}. Tipo: {tipo}. Observaciones: {observaciones}",
                                    )
            return JsonResponse(evento.pk, safe=False)