from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from datetime import datetime
from app import db
from app.models.soporteplus_models import (
    Tiquet, CatTiquet, EstadoTiquet, CatalogoCriticidad,
    Ubicaciones, Usuario, Comentarios
)
from marshmallow import Schema, fields, pre_load, ValidationError

bp = Blueprint('tickets', __name__)


class TiquetSchema(Schema):
    """Schema para serializar tickets"""
    Id_Tiquet = fields.Int(dump_only=True)
    Categoria = fields.Int(allow_none=True)
    Tel_ext = fields.Str(allow_none=True)
    Ubicacion = fields.Int(allow_none=True)
    Criticidad = fields.Int(allow_none=True)
    Descripcion = fields.Str(allow_none=True)
    User_asig = fields.Int(allow_none=True)
    Estado = fields.Int(allow_none=True)
    Fecha_apertura = fields.Raw(allow_none=True)  # Manejado completamente en pre_load
    fecha_apertura_input = fields.Str(load_only=True, allow_none=True)  # Para recibir dd-mm-yyyy
    Fecha_cierre = fields.Raw(allow_none=True, dump_only=True)  # Solo para lectura, se establece automáticamente
    
    # Campos relacionados
    categoria_rel = fields.Nested('CatTiquetSchema', dump_only=True)
    ubicacion_rel = fields.Nested('UbicacionesSchema', dump_only=True)
    criticidad_rel = fields.Nested('CatalogoCriticidadSchema', dump_only=True)
    estado_rel = fields.Nested('EstadoTiquetSchema', dump_only=True)
    usuario_asignado = fields.Nested('UsuarioSchema', dump_only=True)
    
    @pre_load
    def convert_date_format(self, data, **kwargs):
        """Convierte fecha de dd-mm-yyyy a yyyy-mm-dd para la base de datos"""
        if 'fecha_apertura_input' in data and data['fecha_apertura_input']:
            try:
                # Convertir de dd-mm-yyyy a date object
                fecha_input = data['fecha_apertura_input']
                fecha_obj = datetime.strptime(fecha_input, '%d-%m-%Y').date()
                data['Fecha_apertura'] = fecha_obj
                # Remover el campo temporal
                del data['fecha_apertura_input']
            except ValueError:
                raise ValidationError('Fecha debe estar en formato dd-mm-yyyy', 'fecha_apertura_input')
        elif 'Fecha_apertura' not in data or data.get('Fecha_apertura') is None:
            # Si no se proporciona fecha, usar fecha actual
            data['Fecha_apertura'] = datetime.utcnow().date()
        return data


class CatTiquetSchema(Schema):
    """Schema para categorías de tickets"""
    Categoria = fields.Int(dump_only=True)
    Unidad_corresponde = fields.Str(allow_none=True)
    Nombre = fields.Str(allow_none=True)


class EstadoTiquetSchema(Schema):
    """Schema para estados de tickets"""
    ID_estado = fields.Int(dump_only=True)
    Nombre = fields.Str(required=True)
    Descripcion = fields.Str(allow_none=True)


class CatalogoCriticidadSchema(Schema):
    """Schema para criticidad"""
    ID_criti = fields.Int(dump_only=True)
    Nombre = fields.Str(allow_none=True)


class UbicacionesSchema(Schema):
    """Schema para ubicaciones"""
    Id_ubicacion = fields.Int(dump_only=True)
    Nombre = fields.Str(required=True)
    Zona = fields.Str(allow_none=True)


class UsuarioSchema(Schema):
    """Schema para usuarios"""
    ID_usuario = fields.Int(dump_only=True)
    Nombre = fields.Str(required=True)
    ID_Rol = fields.Int(allow_none=True)


# Instanciar schemas
tiquet_schema = TiquetSchema()
tiquets_schema = TiquetSchema(many=True)
cat_tiquet_schema = CatTiquetSchema()
cat_tiquets_schema = CatTiquetSchema(many=True)
estado_schema = EstadoTiquetSchema()
estados_schema = EstadoTiquetSchema(many=True)
criticidad_schema = CatalogoCriticidadSchema()
criticidades_schema = CatalogoCriticidadSchema(many=True)
ubicacion_schema = UbicacionesSchema()
ubicaciones_schema = UbicacionesSchema(many=True)


@bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    """Obtener todos los tickets con sus relaciones cargadas"""
    try:
        # Cargar tickets con todas sus relaciones usando joinedload
        tickets = Tiquet.query.options(
            joinedload(Tiquet.categoria_rel),
            joinedload(Tiquet.ubicacion_rel),
            joinedload(Tiquet.criticidad_rel),
            joinedload(Tiquet.usuario_asignado),
            joinedload(Tiquet.estado_rel)
        ).all()
        
        return jsonify({
            'status': 'success',
            'data': tiquets_schema.dump(tickets),
            'total': len(tickets)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.route('/tickets/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    """Obtener un ticket específico con sus relaciones cargadas"""
    try:
        # Cargar ticket específico con todas sus relaciones
        ticket = Tiquet.query.options(
            joinedload(Tiquet.categoria_rel),
            joinedload(Tiquet.ubicacion_rel),
            joinedload(Tiquet.criticidad_rel),
            joinedload(Tiquet.usuario_asignado),
            joinedload(Tiquet.estado_rel)
        ).filter_by(Id_Tiquet=ticket_id).first()
        
        if not ticket:
            return jsonify({
                'status': 'error',
                'message': 'Ticket not found'
            }), 404
            
        return jsonify({
            'status': 'success',
            'data': tiquet_schema.dump(ticket)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.route('/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    """Crear un nuevo ticket con conversión de fecha"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        # Validar y transformar datos usando el schema
        try:
            validated_data = tiquet_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'status': 'error',
                'message': 'Datos inválidos',
                'errors': err.messages
            }), 400
        
        # Crear ticket con datos validados
        ticket = Tiquet(**validated_data)
        db.session.add(ticket)
        db.session.commit()
        
        # Cargar ticket con relaciones para la respuesta
        ticket_with_relations = Tiquet.query.options(
            joinedload(Tiquet.categoria_rel),
            joinedload(Tiquet.ubicacion_rel),
            joinedload(Tiquet.criticidad_rel),
            joinedload(Tiquet.usuario_asignado),
            joinedload(Tiquet.estado_rel)
        ).filter_by(Id_Tiquet=ticket.Id_Tiquet).first()
        
        return jsonify({
            'status': 'success',
            'message': 'Ticket creado exitosamente',
            'data': tiquet_schema.dump(ticket_with_relations)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error interno del servidor: {str(e)}'
        }), 500


@bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
@jwt_required()
def update_ticket(ticket_id):
    """Actualizar un ticket"""
    try:
        ticket = Tiquet.query.get_or_404(ticket_id)
        data = request.get_json()
        
        # Validar datos
        errors = tiquet_schema.validate(data, partial=True)
        if errors:
            return jsonify({
                'status': 'error',
                'message': 'Datos inválidos',
                'errors': errors
            }), 400
        
        # Actualizar campos
        for key, value in data.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Ticket actualizado exitosamente',
            'data': tiquet_schema.dump(ticket)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@jwt_required()
def delete_ticket(ticket_id):
    """Eliminar un ticket"""
    try:
        ticket = Tiquet.query.get_or_404(ticket_id)
        
        # Opcional: Eliminar registros relacionados primero si es necesario
        # (SQLAlchemy debería manejar esto automáticamente si está configurado en cascade)
        
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Ticket {ticket_id} eliminado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al eliminar ticket: {str(e)}'
        }), 500


@bp.route('/tickets/<int:ticket_id>/close', methods=['PUT'])
@jwt_required()
def close_ticket(ticket_id):
    """Cerrar un ticket - establece fecha de cierre y cambia estado a cerrado"""
    try:
        # Buscar el ticket
        ticket = Tiquet.query.get_or_404(ticket_id)
        
        # Buscar el estado "cerrado" (asumiendo que existe un estado con nombre "Cerrado")
        estado_cerrado = EstadoTiquet.query.filter_by(Nombre='Cerrado').first()
        if not estado_cerrado:
            # Si no encuentra "Cerrado", buscar por variaciones comunes
            estado_cerrado = EstadoTiquet.query.filter(
                EstadoTiquet.Nombre.ilike('%cerrado%') | 
                EstadoTiquet.Nombre.ilike('%closed%') |
                EstadoTiquet.Nombre.ilike('%finalizado%')
            ).first()
        
        if not estado_cerrado:
            return jsonify({
                'status': 'error',
                'message': 'No se encontró un estado de "Cerrado" en el sistema'
            }), 400
        
        # Verificar si el ticket ya está cerrado
        if ticket.Estado == estado_cerrado.ID_estado and ticket.Fecha_cierre:
            return jsonify({
                'status': 'warning',
                'message': 'El ticket ya está cerrado',
                'data': {
                    'Id_Tiquet': ticket.Id_Tiquet,
                    'Estado': ticket.Estado,
                    'Fecha_cierre': ticket.Fecha_cierre.strftime('%d-%m-%Y') if ticket.Fecha_cierre else None
                }
            })
        
        # Cerrar el ticket
        ticket.Estado = estado_cerrado.ID_estado
        ticket.Fecha_cierre = datetime.utcnow().date()
        
        db.session.commit()
        
        # Cargar relaciones para la respuesta
        ticket_with_relations = Tiquet.query.options(
            joinedload(Tiquet.categoria_rel),
            joinedload(Tiquet.ubicacion_rel), 
            joinedload(Tiquet.criticidad_rel),
            joinedload(Tiquet.estado_rel),
            joinedload(Tiquet.usuario_asignado)
        ).get(ticket_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Ticket {ticket_id} cerrado exitosamente',
            'data': {
                'Id_Tiquet': ticket_with_relations.Id_Tiquet,
                'Estado': ticket_with_relations.Estado,
                'Estado_nombre': ticket_with_relations.estado_rel.Nombre if ticket_with_relations.estado_rel else None,
                'Fecha_apertura': ticket_with_relations.Fecha_apertura.strftime('%d-%m-%Y') if ticket_with_relations.Fecha_apertura else None,
                'Fecha_cierre': ticket_with_relations.Fecha_cierre.strftime('%d-%m-%Y') if ticket_with_relations.Fecha_cierre else None,
                'Descripcion': ticket_with_relations.Descripcion
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al cerrar ticket: {str(e)}'
        }), 500


# Rutas para catálogos
@bp.route('/categorias', methods=['GET'])
@jwt_required()
def get_categorias():
    """Obtener todas las categorías"""
    categorias = CatTiquet.query.all()
    return jsonify({
        'status': 'success',
        'data': cat_tiquets_schema.dump(categorias)
    })


@bp.route('/estados', methods=['GET'])
@jwt_required()
def get_estados():
    """Obtener todos los estados"""
    estados = EstadoTiquet.query.all()
    return jsonify({
        'status': 'success',
        'data': estados_schema.dump(estados)
    })


@bp.route('/criticidades', methods=['GET'])
@jwt_required()
def get_criticidades():
    """Obtener todas las criticidades"""
    criticidades = CatalogoCriticidad.query.all()
    return jsonify({
        'status': 'success',
        'data': criticidades_schema.dump(criticidades)
    })


@bp.route('/ubicaciones', methods=['GET'])
@jwt_required()
def get_ubicaciones():
    """Obtener todas las ubicaciones"""
    ubicaciones = Ubicaciones.query.all()
    return jsonify({
        'status': 'success',
        'data': ubicaciones_schema.dump(ubicaciones)
    })


@bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    try:
        total_tickets = Tiquet.query.count()
        tickets_abiertos = Tiquet.query.join(EstadoTiquet).filter(
            EstadoTiquet.Nombre != 'Cerrado'
        ).count()
        tickets_cerrados = total_tickets - tickets_abiertos
        
        # Tickets por estado
        tickets_por_estado = db.session.query(
            EstadoTiquet.Nombre,
            db.func.count(Tiquet.Id_Tiquet)
        ).outerjoin(Tiquet).group_by(EstadoTiquet.ID_estado).all()
        
        # Tickets por criticidad
        tickets_por_criticidad = db.session.query(
            CatalogoCriticidad.Nombre,
            db.func.count(Tiquet.Id_Tiquet)
        ).outerjoin(Tiquet).group_by(CatalogoCriticidad.ID_criti).all()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_tickets': total_tickets,
                'tickets_abiertos': tickets_abiertos,
                'tickets_cerrados': tickets_cerrados,
                'tickets_por_estado': [
                    {'estado': estado, 'cantidad': cantidad}
                    for estado, cantidad in tickets_por_estado
                ],
                'tickets_por_criticidad': [
                    {'criticidad': criticidad, 'cantidad': cantidad}
                    for criticidad, cantidad in tickets_por_criticidad
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500