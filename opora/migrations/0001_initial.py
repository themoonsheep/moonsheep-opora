# Generated by Django 2.0 on 2017-12-18 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.PositiveIntegerField(choices=[(1, 'cash contribution'), (2, 'return in law violation'), (3, 'return in error')], verbose_name='transaction type')),
                ('money_destination', models.PositiveIntegerField(choices=[(1, 'political party account'), (2, 'election fund')], verbose_name='money destination')),
                ('bank_document_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='bank document ID')),
                ('page', models.PositiveIntegerField(blank=True, null=True, verbose_name='page number containing table with transaction')),
                ('receipt_date', models.DateField(blank=True, null=True, verbose_name='receipt date')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='donation amount')),
                ('account_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='account type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_identification', models.SmallIntegerField(choices=[(1, 'individual'), (2, 'legal entity')], verbose_name='legal identification')),
                ('name', models.CharField(max_length=200, verbose_name='payee name (first name + last name + name of the father)')),
                ('identification', models.CharField(max_length=100, verbose_name='payee ID or Passport number')),
                ('address', models.CharField(max_length=200, verbose_name='payee Address')),
            ],
        ),
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('legal_id', models.PositiveIntegerField(verbose_name='local id')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='report URL')),
                ('date', models.DateField(verbose_name='report date')),
                ('finished', models.BooleanField(default=False, verbose_name='object completely translated')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opora.PoliticalParty', verbose_name='related parties')),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.PositiveIntegerField(choices=[(1, 'cash contribution'), (2, 'return in law violation'), (3, 'return in error')], verbose_name='transaction type')),
                ('money_destination', models.PositiveIntegerField(choices=[(1, 'political party account'), (2, 'election fund')], verbose_name='money destination')),
                ('bank_document_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='bank document ID')),
                ('page', models.PositiveIntegerField(blank=True, null=True, verbose_name='page number containing table with transaction')),
                ('receipt_date', models.DateField(blank=True, null=True, verbose_name='receipt date')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='donation amount')),
                ('date', models.DateField(blank=True, null=True, verbose_name='return date')),
                ('document_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='return document id')),
                ('explanation', models.TextField(blank=True, null=True, verbose_name='return explanation')),
                ('amount_to_payee', models.PositiveIntegerField(blank=True, null=True, verbose_name='return amount to payee')),
                ('amount_to_state_budget', models.PositiveIntegerField(blank=True, null=True, verbose_name='return amount to state budget')),
                ('payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opora.Payee', verbose_name='payee')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opora.Report', verbose_name='report')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_start', models.PositiveIntegerField(blank=True, null=True, verbose_name='document first page containing table')),
                ('page_end', models.PositiveIntegerField(blank=True, null=True, verbose_name='document last page containing table')),
                ('transaction_type', models.PositiveIntegerField(choices=[(1, 'cash contribution'), (2, 'return in law violation'), (3, 'return in error')], verbose_name='transaction type')),
                ('money_destination', models.PositiveIntegerField(choices=[(1, 'political party account'), (2, 'election fund')], verbose_name='money destination')),
                ('legal_identification', models.SmallIntegerField(choices=[(1, 'individual'), (2, 'legal entity')], verbose_name='legal identification')),
                ('total_funds', models.PositiveIntegerField(blank=True, null=True, verbose_name='total funds received')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opora.Report', verbose_name='report')),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='payee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opora.Payee', verbose_name='payee'),
        ),
        migrations.AddField(
            model_name='donation',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opora.Report', verbose_name='report'),
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('date', 'party')},
        ),
    ]
