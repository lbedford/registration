# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lbw'
        db.create_table(u'registration_lbw', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('lbw_url', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal(u'registration', ['Lbw'])

        # Adding M2M table for field owners on 'Lbw'
        m2m_table_name = db.shorten_name(u'registration_lbw_owners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lbw', models.ForeignKey(orm[u'registration.lbw'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lbw_id', 'user_id'])

        # Adding model 'Activity'
        db.create_table(u'registration_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=60)),
            ('preferred_days', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activity_type', self.gf('django.db.models.fields.IntegerField')(default=6)),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activity', null=True, to=orm['registration.Lbw'])),
        ))
        db.send_create_signal(u'registration', ['Activity'])

        # Adding M2M table for field attendees on 'Activity'
        m2m_table_name = db.shorten_name(u'registration_activity_attendees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'registration.activity'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'user_id'])

        # Adding M2M table for field owners on 'Activity'
        m2m_table_name = db.shorten_name(u'registration_activity_owners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'registration.activity'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'user_id'])

        # Adding model 'Accomodation'
        db.create_table(u'registration_accomodation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Lbw'])),
            ('kind', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'registration', ['Accomodation'])

        # Adding model 'UserRegistration'
        db.create_table(u'registration_userregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Lbw'])),
            ('arrival_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('departure_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('accomodation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Accomodation'], null=True, blank=True)),
            ('children', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'registration', ['UserRegistration'])

        # Adding model 'Message'
        db.create_table(u'registration_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Activity'], null=True, blank=True)),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Lbw'], null=True, blank=True)),
            ('next', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next_message', null=True, to=orm['registration.Message'])),
            ('previous', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='previous_message', null=True, to=orm['registration.Message'])),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'registration', ['Message'])

        # Adding model 'Ride'
        db.create_table(u'registration_ride', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ride_from', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ride_to', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('offerer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ride_offerer', to=orm['auth.User'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ride_requester', to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Lbw'])),
        ))
        db.send_create_signal(u'registration', ['Ride'])

        # Adding model 'Tshirt'
        db.create_table(u'registration_tshirt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Lbw'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'registration', ['Tshirt'])

        # Adding model 'TshirtOrders'
        db.create_table(u'registration_tshirtorders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tshirt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Tshirt'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal(u'registration', ['TshirtOrders'])


    def backwards(self, orm):
        # Deleting model 'Lbw'
        db.delete_table(u'registration_lbw')

        # Removing M2M table for field owners on 'Lbw'
        db.delete_table(db.shorten_name(u'registration_lbw_owners'))

        # Deleting model 'Activity'
        db.delete_table(u'registration_activity')

        # Removing M2M table for field attendees on 'Activity'
        db.delete_table(db.shorten_name(u'registration_activity_attendees'))

        # Removing M2M table for field owners on 'Activity'
        db.delete_table(db.shorten_name(u'registration_activity_owners'))

        # Deleting model 'Accomodation'
        db.delete_table(u'registration_accomodation')

        # Deleting model 'UserRegistration'
        db.delete_table(u'registration_userregistration')

        # Deleting model 'Message'
        db.delete_table(u'registration_message')

        # Deleting model 'Ride'
        db.delete_table(u'registration_ride')

        # Deleting model 'Tshirt'
        db.delete_table(u'registration_tshirt')

        # Deleting model 'TshirtOrders'
        db.delete_table(u'registration_tshirtorders')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registration.accomodation': {
            'Meta': {'object_name': 'Accomodation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Lbw']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'registration.activity': {
            'Meta': {'object_name': 'Activity'},
            'activity_type': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'activity_attendees'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activity'", 'null': 'True', 'to': u"orm['registration.Lbw']"}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activity_owners'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'preferred_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'registration.lbw': {
            'Meta': {'object_name': 'Lbw'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'lbw_attendees'", 'blank': 'True', 'through': u"orm['registration.UserRegistration']", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw_url': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'lbw_owners'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'registration.message': {
            'Meta': {'object_name': 'Message'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Activity']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Lbw']", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next_message'", 'null': 'True', 'to': u"orm['registration.Message']"}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_message'", 'null': 'True', 'to': u"orm['registration.Message']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'registration.ride': {
            'Meta': {'object_name': 'Ride'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Lbw']"}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'offerer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ride_offerer'", 'to': u"orm['auth.User']"}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ride_requester'", 'to': u"orm['auth.User']"}),
            'ride_from': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ride_to': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registration.tshirt': {
            'Meta': {'object_name': 'Tshirt'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Lbw']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        u'registration.tshirtorders': {
            'Meta': {'object_name': 'TshirtOrders'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'tshirt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Tshirt']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'registration.userregistration': {
            'Meta': {'object_name': 'UserRegistration'},
            'accomodation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Accomodation']", 'null': 'True', 'blank': 'True'}),
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {}),
            'children': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'departure_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lbw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Lbw']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['registration']