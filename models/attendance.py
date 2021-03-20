
import time
from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta as rd
from odoo.exceptions import ValidationError
from lxml import etree
import json

class AttendanceSheet(models.Model):
    '''Defining Monthly Attendance sheet Information.'''

    _description = 'Attendance Sheet'
    _name = 'attendance.sheet'

    name = fields.Char('Mô tả',)
    month_id = fields.Many2one('attendance.month', 'Tháng', required=True,)
    year_id = fields.Many2one('attendance.year', 'Năm', required=True)
    attendance_ids = fields.One2many('attendance.sheet.line', 'standard_id',
                                     'Danh sách chấm công',)
    user_id = fields.Many2one('res.user', 'Người chấm công')
    # attendance_type = fields.Selection([('daily', 'FullDay'),
    #                                     ('lecture', 'Lecture Wise')], 'Type')

    @api.model
    def fields_view_get(self, view_id=None,
                        view_type='form',
                        toolbar=False, submenu=False):
        res = super(AttendanceSheet, self).fields_view_get(view_id=view_id,
                                                           view_type=view_type,
                                                           toolbar=toolbar,
                                                           submenu=submenu)
        start = self._context.get('start_date')
        end = self._context.get('end_date')
        st_dates = end_dates = False
        if start:
            st_dates = datetime.strptime(start,
                                         DEFAULT_SERVER_DATE_FORMAT)
        if end:
            end_dates = datetime.strptime(end,
                                          DEFAULT_SERVER_DATE_FORMAT)
        # if view_type == 'form':
        #     digits_temp_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four',
        #                         5: 'five', 6: 'six', 7: 'seven', 8: 'eight',
        #                         9: 'nine', 10: 'ten', 11: 'one_1', 12: 'one_2',
        #                         13: 'one_3', 14: 'one_4', 15: 'one_5',
        #                         16: 'one_6', 17: 'one_7', 18: 'one_8',
        #                         19: 'one_9', 20: 'one_0',
        #                         21: 'two_1', 22: 'two_2', 23: 'two_3',
        #                         24: 'two_4', 25: 'two_5',
        #                         26: 'two_6', 27: 'two_7', 28: 'two_8',
        #                         29: 'two_9', 30: 'two_0',
        #                         31: 'three_1'}
        #     flag = 1
        #     if st_dates and end_dates:
        #         while st_dates <= end_dates:
        #             res['fields']['attendance_ids'
        #                           ]['views'
        #                             ]['tree'
        #                               ]['fields'
        #                                 ][digits_temp_dict.get(flag)
        #                                   ]['string'
        #                                     ] = st_dates.day
        #             st_dates += rd(days=1)
        #             flag += 1
        #     if flag < 32:
        #         res['fields']['attendance_ids'
        #                       ]['views']['tree'
        #                                  ]['fields'
        #                                    ][digits_temp_dict.get(flag)
        #                                      ]['string'] = ''
        #         doc2 = etree.XML(res['fields']['attendance_ids']['views'
        #                                                          ]['tree'
        #                                                            ]['arch'])
        #         nodes = doc2.xpath("//field[@name='" +
        #                            digits_temp_dict.get(flag) + "']")
        #         for node in nodes:
        #             node.set('modifiers', json.dumps({'invisible': True}))
        #         res['fields']['attendance_ids'
        #                       ]['views']['tree']['arch'] = etree.tostring(doc2)
        return res
class Attendance(models.Model):
    _description = 'Attendance Sheet Line'
    _name = 'attendance.sheet.line'
    _order = 'roll_no'

    def _compute_percentage(self):
        '''Method to get attendance percent.'''

        res = {}
        for attendance_sheet_data in self:
            att_count = 0
            percentage = 0.0
            if attendance_sheet_data.one:
                att_count = att_count + 1
            if attendance_sheet_data.two:
                att_count = att_count + 1
            if attendance_sheet_data.three:
                att_count = att_count + 1
            if attendance_sheet_data.four:
                att_count = att_count + 1
            if attendance_sheet_data.five:
                att_count = att_count + 1
            if attendance_sheet_data.six:
                att_count = att_count + 1
            if attendance_sheet_data.seven:
                att_count = att_count + 1
            if attendance_sheet_data.eight:
                att_count = att_count + 1
            if attendance_sheet_data.nine:
                att_count = att_count + 1
            if attendance_sheet_data.ten:
                att_count = att_count + 1

            if attendance_sheet_data.one_1:
                att_count = att_count + 1
            if attendance_sheet_data.one_2:
                att_count = att_count + 1
            if attendance_sheet_data.one_3:
                att_count = att_count + 1
            if attendance_sheet_data.one_4:
                att_count = att_count + 1
            if attendance_sheet_data.one_5:
                att_count = att_count + 1
            if attendance_sheet_data.one_6:
                att_count = att_count + 1
            if attendance_sheet_data.one_7:
                att_count = att_count + 1
            if attendance_sheet_data.one_8:
                att_count = att_count + 1
            if attendance_sheet_data.one_9:
                att_count = att_count + 1
            if attendance_sheet_data.one_0:
                att_count = att_count + 1

            if attendance_sheet_data.two_1:
                att_count = att_count + 1
            if attendance_sheet_data.two_2:
                att_count = att_count + 1
            if attendance_sheet_data.two_3:
                att_count = att_count + 1
            if attendance_sheet_data.two_4:
                att_count = att_count + 1
            if attendance_sheet_data.two_5:
                att_count = att_count + 1
            if attendance_sheet_data.two_6:
                att_count = att_count + 1
            if attendance_sheet_data.two_7:
                att_count = att_count + 1
            if attendance_sheet_data.two_8:
                att_count = att_count + 1
            if attendance_sheet_data.two_9:
                att_count = att_count + 1
            if attendance_sheet_data.two_0:
                att_count = att_count + 1
            if attendance_sheet_data.three_1:
                att_count = att_count + 1
            percentage = (float(att_count / 31.00)) * 100
            attendance_sheet_data.percentage = percentage
        return res

    roll_no = fields.Integer('STT', required=True,
                             help='Roll Number of Student')
    standard_id = fields.Many2one('attendance.sheet', 'Standard')
    name = fields.Many2one('hr.employee','Nhân viên', required=True)
    position = fields.Char('Chức vụ', compute="get_position")
    month = fields.Integer(compute="get_month")
    
    @api.onchange('standard_id')
    def get_month(self):
        for rec in self:
            rec.month = rec.standard_id.month_id.name
            print("=============")
            print(rec.month)
            
    @api.depends('name')
    def get_position(self):
        for rec in self:
            rec.position = rec.name.job_title

    def get_symbol_default(self):
        self.three.name = '+'

    one = fields.Many2one('attendance.symbol', '1')
    two = fields.Many2one('attendance.symbol', '2')
    three = fields.Many2one('attendance.symbol', '3')
    four = fields.Many2one('attendance.symbol', '4')
    five = fields.Many2one('attendance.symbol', '5')
    seven = fields.Many2one('attendance.symbol', '6')
    six = fields.Many2one('attendance.symbol', '7')
    eight = fields.Many2one('attendance.symbol', '8')
    nine = fields.Many2one('attendance.symbol', '9')
    ten = fields.Many2one('attendance.symbol', '10')
    one_1 = fields.Many2one('attendance.symbol', '11')
    one_2 = fields.Many2one('attendance.symbol', '12')
    one_3 = fields.Many2one('attendance.symbol', '13')
    one_4 = fields.Many2one('attendance.symbol', '14')
    one_5 = fields.Many2one('attendance.symbol', '15')
    one_6 = fields.Many2one('attendance.symbol', '16')
    one_7 = fields.Many2one('attendance.symbol', '17')
    one_8 = fields.Many2one('attendance.symbol', '18')
    one_9 = fields.Many2one('attendance.symbol', '19')
    one_0 = fields.Many2one('attendance.symbol', '20')
    two_1 = fields.Many2one('attendance.symbol', '21')
    two_2 = fields.Many2one('attendance.symbol', '22')
    two_3 = fields.Many2one('attendance.symbol', '23')
    two_4 = fields.Many2one('attendance.symbol', '24')
    two_5 = fields.Many2one('attendance.symbol', '25')
    two_6 = fields.Many2one('attendance.symbol', '26')
    two_7 = fields.Many2one('attendance.symbol', '27')
    two_8 = fields.Many2one('attendance.symbol', '28')
    two_9 = fields.Many2one('attendance.symbol', '29')
    two_0 = fields.Many2one('attendance.symbol', '30')
    three_1 = fields.Many2one('attendance.symbol', '31')
    percentage = fields.Float(compute="_compute_percentage", method=True,
                              string='Ngày công (%)', store=False)
    
class AttendanceYear(models.Model):
    '''Defines an academic year.'''

    _name = "attendance.year"
    _description = "Academic Year"
    _order = "sequence"

    sequence = fields.Integer('Số TT', required=True,
                              help="Sequence order you want to see this year.")
    name = fields.Char('Năm', required=True, help='Name of academic year')
    date_start = fields.Date('Ngày bắt đầu', required=True,
                             help='Ngày bắt dầu của năm')
    date_stop = fields.Date('Ngày kết thúc', required=True,
                            help='Ngày kết thúc năm')
    month_ids = fields.One2many('attendance.month', 'year_id', 'Tháng',
                                help="related Academic months")
    current = fields.Boolean('Năm hiện tại', help="Năm hiện tại")
    description = fields.Text('Mô tả')

    @api.model
    def next_year(self, sequence):
        '''This method assign sequence to years'''
        year_id = self.search([('sequence', '>', sequence)], order='id',
                              limit=1)
        if year_id:
            return year_id.id
        return False

    # def name_get(self):
    #     '''Method to display name and code'''
    #     return [(rec.id, ' [' + rec.code + ']' + rec.name) for rec in self]

    def generate_academicmonth(self):
        """Generate academic months."""
        interval = 1
        month_obj = self.env['academic.month']
        for data in self:
            ds = data.date_start
            while ds < data.date_stop:
                de = ds + relativedelta(months=interval, days=-1)
                if de > data.date_stop:
                    de = data.date_stop
                month_obj.create({
                    'name': ds.strftime('%B'),
                    'code': ds.strftime('%m/%Y'),
                    'date_start': ds.strftime('%Y-%m-%d'),
                    'date_stop': de.strftime('%Y-%m-%d'),
                    'year_id': data.id,
                })
                ds = ds + relativedelta(months=interval)
        return True

    @api.constrains('date_start', 'date_stop')
    def _check_academic_year(self):
        '''Method to check start date should be greater than end date
           also check that dates are not overlapped with existing academic
           year'''
        new_start_date = self.date_start
        new_stop_date = self.date_stop
        delta = new_stop_date - new_start_date
        if delta.days > 365 and not calendar.isleap(new_start_date.year):
            raise ValidationError(_('''Error! The duration of the academic year
                                      is invalid.'''))
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_('''The start date of the academic year'
                                      should be less than end date.'''))
        for old_ac in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_ac.date_start <= self.date_start <= old_ac.date_stop or
                    old_ac.date_start <= self.date_stop <= old_ac.date_stop):
                raise ValidationError(_('''Error! You cannot define overlapping
                                          academic years.'''))

    @api.constrains('current')
    def check_current_year(self):
        check_year = self.search([('current', '=', True)])
        if len(check_year.ids) >= 2:
            raise ValidationError(_('''Error! You cannot set two current \
year active!'''))


class AttendanceMonth(models.Model):
    '''Defining a month of an academic year.'''

    _name = "attendance.month"
    _description = "Academic Month"
    _order = "name"
    _rec_name = "name"

    name = fields.Integer('Name', required=True, help='Name of Academic month')
    # code = fields.Char('Code', required=True, help='Code of Academic month')
    date_start = fields.Date('Start of Period', required=True,
                             help='Starting of academic month')
    date_stop = fields.Date('End of Period', required=True,
                            help='Ending of academic month')
    year_id = fields.Many2one('attendance.year', 'Academic Year', required=True,
                              help="Related academic year ")
    description = fields.Text('Description')

    _sql_constraints = [
        ('month_unique', 'unique(date_start, date_stop, year_id)',
         'Academic Month should be unique!'),
    ]

    @api.constrains('date_start', 'date_stop')
    def _check_duration(self):
        '''Method to check duration of date'''
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_(''' End of Period date should be greater
                                    than Start of Peroid Date!'''))

    @api.constrains('year_id', 'date_start', 'date_stop')
    def _check_year_limit(self):
        '''Method to check year limit'''
        if self.year_id and self.date_start and self.date_stop:
            if (self.year_id.date_stop < self.date_stop or
                    self.year_id.date_stop < self.date_start or
                    self.year_id.date_start > self.date_start or
                    self.year_id.date_start > self.date_stop):
                raise ValidationError(_('''Invalid Months ! Some months overlap
                                    or the date period is not in the scope
                                    of the academic year!'''))

    @api.constrains('date_start', 'date_stop')
    def check_months(self):
        """Check start date should be less than stop date."""
        for old_month in self.search([('id', 'not in', self.ids)]):
            if old_month.date_start <= \
                    self.date_start <= old_month.date_stop \
                    or old_month.date_start <= \
                    self.date_stop <= old_month.date_stop:
                raise ValidationError(_('''Error! You cannot define
                    overlapping months!'''))
class AttendanceSymbol(models.Model):
    '''Defining Attendance Symbol.'''
    _name = "attendance.symbol"
    _description = "Attendance Symbol"
    _order = "name"
    _rec_name = "name"

    name = fields.Char("Kí hiệu")
    description = fields.Char("Mô tả")
    workday = fields.Float("Ngày công")