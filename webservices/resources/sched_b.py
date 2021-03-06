import sqlalchemy as sa
from flask_apispec import doc, marshal_with

from webservices import args
from webservices import docs
from webservices import schemas
from webservices.common import models
from webservices.utils import use_kwargs
from webservices.common.views import ItemizedResource


@doc(
    tags=['schedules/schedule_b'],
    description=docs.SCHEDULE_B,
)
class ScheduleBView(ItemizedResource):

    model = models.ScheduleB

    @property
    def year_column(self):
        return self.model.report_year
    @property
    def index_column(self):
        return self.model.sched_b_sk

    filter_multi_fields = [
        ('image_number', models.ScheduleB.image_number),
        ('committee_id', models.ScheduleB.committee_id),
        ('recipient_city', models.ScheduleB.recipient_city),
        ('recipient_state', models.ScheduleB.recipient_state),
        ('recipient_committee_id', models.ScheduleB.recipient_committee_id),
    ]
    filter_fulltext_fields = [
        ('recipient_name', models.ScheduleB.recipient_name_text),
        ('disbursement_description', models.ScheduleB.disbursement_description_text),
    ]
    filter_range_fields = [
        (('min_date', 'max_date'), models.ScheduleB.disbursement_date),
        (('min_amount', 'max_amount'), models.ScheduleB.disbursement_amount),
        (('min_image_number', 'max_image_number'), models.ScheduleB.image_number),
    ]

    @use_kwargs(args.itemized)
    @use_kwargs(args.schedule_b)
    @use_kwargs(args.make_seek_args())
    @use_kwargs(
        args.make_sort_args(
            validator=args.OptionValidator(['disbursement_date', 'disbursement_amount']),
            multiple=False,
        )
    )
    @marshal_with(schemas.ScheduleBPageSchema())
    def get(self, **kwargs):
        return super().get(**kwargs)

    def build_query(self, **kwargs):
        query = super(ScheduleBView, self).build_query(**kwargs)
        query = query.options(sa.orm.joinedload(models.ScheduleB.committee))
        query = query.options(sa.orm.joinedload(models.ScheduleB.recipient_committee))
        return query
