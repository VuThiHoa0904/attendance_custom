
import time
from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta as rd
from odoo.exceptions import ValidationError
from lxml import etree
import pandas as pd
import json

class AttendanceSheet(models.Model):
    '''Defining Monthly Attendance sheet Information.'''

    _description = 'Attendance Sheet'
    _name = 'attendance.sheet'

    name = fields.Char('Mô tả',)
    # month_id = fields.Many2one('attendance.month', 'Tháng', required=True, domain="[('year_id', '=?', year_id)]")
    month = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                              ('12', '12')], 'Tháng', required=True)
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
class AttendanceLine(models.Model):
    _description = 'Attendance Sheet Line'
    _name = 'attendance.sheet.line'
    _order = 'roll_no'

    def _compute_percentage(self):
        '''Method to get attendance percent.'''

        res = {}
        for attendance_sheet_data in self:
            att_count = 0.0
            # percentage = 0.0
            if attendance_sheet_data.one.workday:
                att_count = att_count + attendance_sheet_data.one.workday
            if attendance_sheet_data.two:
                att_count = att_count + attendance_sheet_data.two.workday
            if attendance_sheet_data.three:
                att_count = att_count + attendance_sheet_data.three.workday
            if attendance_sheet_data.four:
                att_count = att_count + attendance_sheet_data.four.workday
            if attendance_sheet_data.five:
                att_count = att_count + attendance_sheet_data.five.workday
            if attendance_sheet_data.six:
                att_count = att_count + attendance_sheet_data.six.workday
            if attendance_sheet_data.seven:
                att_count = att_count + attendance_sheet_data.seven.workday
            if attendance_sheet_data.eight:
                att_count = att_count + attendance_sheet_data.eight.workday
            if attendance_sheet_data.nine:
                att_count = att_count + attendance_sheet_data.nine.workday
            if attendance_sheet_data.ten:
                att_count = att_count + attendance_sheet_data.ten.workday

            if attendance_sheet_data.one_1:
                att_count = att_count + attendance_sheet_data.one_1.workday
            if attendance_sheet_data.one_2:
                att_count = att_count + attendance_sheet_data.one_2.workday
            if attendance_sheet_data.one_3:
                att_count = att_count + attendance_sheet_data.one_3.workday
            if attendance_sheet_data.one_4:
                att_count = att_count + attendance_sheet_data.one_4.workday
            if attendance_sheet_data.one_5:
                att_count = att_count + attendance_sheet_data.one_5.workday
            if attendance_sheet_data.one_6:
                att_count = att_count + attendance_sheet_data.one_6.workday
            if attendance_sheet_data.one_7:
                att_count = att_count + attendance_sheet_data.one_7.workday
            if attendance_sheet_data.one_8:
                att_count = att_count + attendance_sheet_data.one_8.workday
            if attendance_sheet_data.one_9:
                att_count = att_count + attendance_sheet_data.one_9.workday
            if attendance_sheet_data.one_0:
                att_count = att_count + attendance_sheet_data.one_0.workday

            if attendance_sheet_data.two_1:
                att_count = att_count + attendance_sheet_data.two_1.workday
            if attendance_sheet_data.two_2:
                att_count = att_count + attendance_sheet_data.two_2.workday
            if attendance_sheet_data.two_3:
                att_count = att_count + attendance_sheet_data.two_3.workday
            if attendance_sheet_data.two_4:
                att_count = att_count + attendance_sheet_data.two_4.workday
            if attendance_sheet_data.two_5:
                att_count = att_count + attendance_sheet_data.two_5.workday
            if attendance_sheet_data.two_6:
                att_count = att_count + attendance_sheet_data.two_6.workday
            if attendance_sheet_data.two_7:
                att_count = att_count + attendance_sheet_data.two_7.workday
            if attendance_sheet_data.two_8:
                att_count = att_count + attendance_sheet_data.two_8.workday
            if attendance_sheet_data.two_9:
                att_count = att_count + attendance_sheet_data.two_9.workday
            if attendance_sheet_data.two_0:
                att_count = att_count + attendance_sheet_data.two_0.workday
            if attendance_sheet_data.three_1:
                att_count = att_count + attendance_sheet_data.three_1.workday
            # percentage = (float(att_count / 31.00)) * 100
            attendance_sheet_data.percentage = att_count
        return res

    roll_no = fields.Integer('STT', required=True,
                             help='Roll Number of Student')
    standard_id = fields.Many2one('attendance.sheet', 'Standard')
    name = fields.Many2one('hr.employee','Nhân viên', required=True)
    position = fields.Char('Chức vụ', compute="get_position")
    month = fields.Selection(related='standard_id.month')
    year = fields.Integer(related='standard_id.year_id.name')
    hide = fields.Boolean(compute="checkYear")
    
    @api.model
    def create(self, days):
        days.update({'year': days.get('year')})
        days.update({'month': days.get('month')})
        CN = self.env['attendance.symbol'].search([('name','=','CN')],limit=1).id
        NL = self.env['attendance.symbol'].search([('name','=','NL')],limit=1).id
        attendance = self.env['attendance.sheet'].search([('id','=',days['standard_id'])],limit=1)
        arr = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'one_1', 'one_2', 'one_3', 'one_4', 'one_5', 'one_6', 'one_7',
           'one_8', 'one_9', 'one_0', 'two_1', 'two_2', 'two_3', 'two_4', 'two_5', 'two_6', 'two_7', 'two_8', 'two_9', 'two_0', 'three_1']
        a = [1, 3, 5, 7, 8, 10, 12]
        b = [4, 6, 9, 11]
        year = attendance.year_id.name
        month = int(attendance.month)
        if month in a:
            for i in range(0,len(arr)):
                day = self._fields[arr[i]].string
                if self.checkDay(year, month, day) == 'Sunday':
                    days[arr[i]] = CN
                if ((month == 5) and (day == '1')) or ((month == 1) and (day == '1')):
                    days[arr[i]] = NL
        if month in b:
            for i in range(0,len(arr)-1):
                day = self._fields[arr[i]].string
                if self.checkDay(year, month, day) == 'Sunday':
                    print("============")
                    print(day)
                    print(month)
                    print(year)
                    days[arr[i]] = CN
                if ((month == 4) and (day == '30')) or ((month == 9) and (day == '2')):
                    days[arr[i]] = NL
        if month == 2:
            if (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)):
                for i in range(0, len(arr)-2):
                    day = self._fields[arr[i]].string
                    if self.checkDay(year, month, day) == 'Sunday':
                        days[arr[i]] = CN
            else:
                for i in range(0, len(arr)-3):
                    day = self._fields[arr[i]].string
                    if self.checkDay(year, month, day) == 'Sunday':
                        days[arr[i]] = CN
        result = super(AttendanceLine, self).create(days)
        return result

    
    def checkDay(self, year, month, day):
        date = pd.DataFrame({'inputDate': [str(year)+'-'+str(month)+'-'+str(day)]})
        date['inputDate'] = pd.to_datetime(date['inputDate'])
        date['dayOfWeek'] = date['inputDate'].dt.day_name()
        return date['dayOfWeek'].values[0]

    # @api.onchange('standard_id.month_id.name')
    @api.model
    def get_symbol(self):
        for rec in self:
            if rec.checkDay(rec.year, rec.month, rec._fields['seven'].string) == 'Sunday':
                rec.seven.name = 'CN'
    @api.model
    @api.depends('year')
    def checkYear(self):
        for rec in self:
            if (((rec.year % 4 == 0) and (rec.year % 100 != 0)) or (rec.year % 400 == 0)):
                rec.hide = True
            else:
                rec.hide = False

    @api.depends('name')
    def get_position(self):
        for rec in self:
            rec.position = rec.name.job_title

    _defaults = {
        'one': lambda *a: '+'
    }

    one = fields.Many2one('attendance.symbol', '1')
    two = fields.Many2one('attendance.symbol', '2')
    three = fields.Many2one('attendance.symbol', '3')
    four = fields.Many2one('attendance.symbol', '4')
    five = fields.Many2one('attendance.symbol', '5')
    six = fields.Many2one('attendance.symbol', '6')
    seven = fields.Many2one('attendance.symbol', '7')
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
                              string='Ngày công', store=False)
    
class AttendanceYear(models.Model):
    '''Defines an academic year.'''

    _name = "attendance.year"
    _description = "Academic Year"
    _order = "sequence"

    sequence = fields.Integer('Số TT', required=True,
                              help="Sắp xếp theo số thứ tự")
    name = fields.Integer('Năm', required=True, help='Tên năm muốn nhập')
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

    # def generate_academicmonth(self):
    #     """Generate academic months."""
    #     interval = 1
    #     month_obj = self.env['academic.month']
    #     for data in self:
    #         ds = data.date_start
    #         while ds < data.date_stop:
    #             de = ds + relativedelta(months=interval, days=-1)
    #             if de > data.date_stop:
    #                 de = data.date_stop
    #             month_obj.create({
    #                 'name': ds.strftime('%B'),
    #                 'code': ds.strftime('%m/%Y'),
    #                 'date_start': ds.strftime('%Y-%m-%d'),
    #                 'date_stop': de.strftime('%Y-%m-%d'),
    #                 'year_id': data.id,
    #             })
    #             ds = ds + relativedelta(months=interval)
    #     return True

    # @api.constrains('date_start', 'date_stop')
    # def _check_academic_year(self):
    #     '''Method to check start date should be greater than end date
    #        also check that dates are not overlapped with existing academic
    #        year'''
    #     new_start_date = self.date_start
    #     new_stop_date = self.date_stop
    #     delta = new_stop_date - new_start_date
    #     if delta.days > 365 and not calendar.isleap(new_start_date.year):
    #         raise ValidationError(_('''Error! The duration of the academic year
    #                                   is invalid.'''))
    #     if (self.date_stop and self.date_start and
    #             self.date_stop < self.date_start):
    #         raise ValidationError(_('''The start date of the academic year'
    #                                   should be less than end date.'''))
    #     for old_ac in self.search([('id', 'not in', self.ids)]):
    #         # Check start date should be less than stop date
    #         if (old_ac.date_start <= self.date_start <= old_ac.date_stop or
    #                 old_ac.date_start <= self.date_stop <= old_ac.date_stop):
    #             raise ValidationError(_('''Error! You cannot define overlapping
    #                                       academic years.'''))

    @api.constrains('current')
    def check_current_year(self):
        check_year = self.search([('current', '=', True)])
        if len(check_year.ids) >= 2:
            raise ValidationError(_('''Error! You cannot set two current \
year active!'''))


# class AttendanceMonth(models.Model):
#     '''Defining a month of an academic year.'''
#
#     _name = "attendance.month"
#     _description = "Academic Month"
#     _order = "name"
#     _rec_name = "name"
#
#     name = fields.Integer('Tháng', required=True, help='Name of Academic month')
#     # code = fields.Char('Code', required=True, help='Code of Academic month')
#     date_start = fields.Date('Ngày bắt đầu',
#                              help='')
#     date_stop = fields.Date('Ngày kết thúc',
#                             help='')
#     year_id = fields.Many2one('attendance.year', 'Năm', required=True,
#                               help=" ")
#     description = fields.Text('Mô tả')
#
#     _sql_constraints = [
#         ('month_unique', 'unique(date_start, date_stop, year_id)',
#          'Academic Month should be unique!'),
#     ]
#
#     @api.constrains('date_start', 'date_stop')
#     def _check_duration(self):
#         '''Method to check duration of date'''
#         if (self.date_stop and self.date_start and
#                 self.date_stop < self.date_start):
#             raise ValidationError(_(''' End of Period date should be greater
#                                     than Start of Peroid Date!'''))
#
#     @api.constrains('year_id', 'date_start', 'date_stop')
#     def _check_year_limit(self):
#         '''Method to check year limit'''
#         if self.year_id and self.date_start and self.date_stop:
#             if (self.year_id.date_stop < self.date_stop or
#                     self.year_id.date_stop < self.date_start or
#                     self.year_id.date_start > self.date_start or
#                     self.year_id.date_start > self.date_stop):
#                 raise ValidationError(_('''Invalid Months ! Some months overlap
#                                     or the date period is not in the scope
#                                     of the academic year!'''))
#
#     @api.constrains('date_start', 'date_stop')
#     def check_months(self):
#         """Check start date should be less than stop date."""
#         for old_month in self.search([('id', 'not in', self.ids)]):
#             if old_month.date_start <= \
#                     self.date_start <= old_month.date_stop \
#                     or old_month.date_start <= \
#                     self.date_stop <= old_month.date_stop:
#                 raise ValidationError(_('''Error! You cannot define
#                     overlapping months!'''))


class AttendanceSymbol(models.Model):
    '''Defining Attendance Symbol.'''
    _name = "attendance.symbol"
    _description = "Attendance Symbol"
    _order = "name"
    _rec_name = "name"

    name = fields.Char("Kí hiệu")
    description = fields.Char("Mô tả")
    workday = fields.Float("Ngày công")

class PartnerXlsx(models.AbstractModel):
    _name = 'report.attendance_custom.attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    def checkYear(self, year):
        return (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0))

    def getDay(self, year, month, day):
        date = pd.DataFrame({'inputDate': [str(year)+'-'+str(month)+'-'+str(day)]})
        date['inputDate'] = pd.to_datetime(date['inputDate'])
        date['dayOfWeek'] = date['inputDate'].dt.day_name()
        if date['dayOfWeek'].values[0] == 'Monday':
            date['dayOfWeek'].values[0] = 'T2'
        if date['dayOfWeek'].values[0] == 'Tuesday':
            date['dayOfWeek'].values[0] = 'T3'
        if date['dayOfWeek'].values[0] == 'Wednesday':
            date['dayOfWeek'].values[0] = 'T4'
        if date['dayOfWeek'].values[0] == 'Thursday':
            date['dayOfWeek'].values[0] = 'T5'
        if date['dayOfWeek'].values[0] == 'Friday':
            date['dayOfWeek'].values[0] = 'T6'
        if date['dayOfWeek'].values[0] == 'Saturday':
            date['dayOfWeek'].values[0] = 'T7'
        if date['dayOfWeek'].values[0] == 'Sunday':
            date['dayOfWeek'].values[0] = 'CN'
        return date['dayOfWeek'].values[0]

    def generate_xlsx_report(self, workbook, data, lines):
        for obj in lines:
            report_name = obj.name

            # Tạo sheet mới
            sheet = workbook.add_worksheet(report_name[:31])

            name_header = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'font_color': 'red', 'font_name': 'Times New Roman'})
            sheet.set_row(0, 30)
            sheet.merge_range('A1:AI1', 'BẢNG CHẤM CÔNG', name_header)
            date_header = workbook.add_format({'font_size': 15, 'align': 'center', 'bold': True, 'font_color': 'red', 'font_name': 'Times New Roman'})
            sheet.set_row(1, 20)
            sheet.merge_range('A2:AI2', 'Tháng ' + obj.month+' Năm ' + str(obj.year_id.name), date_header)

            # Tiêu đề cột
            title = workbook.add_format({'font_size': 12, 'align': 'center','bold': True, 'border': 1, 'font_color': 'black', 'font_name': 'Times New Roman','bg_color':'#00FFFF'})
            sheet.merge_range('A3:A5', 'TT', title)
            sheet.set_column('A3:A5', 3)
            sheet.merge_range('B3:B5', 'Họ và tên', title)
            sheet.set_column('B3:B5', 20)
            sheet.merge_range('C3:C5', 'Chức vụ/ Bộ phận', title)
            sheet.set_column('C3:C5', 25)
            sheet.set_row(2, 20)
            sheet.merge_range('D3:AI3', 'Ngày trong tháng', title)
            sheet.set_column('AI4:AI5', 25)
            sheet.merge_range('AI4:AI5', 'Tổng cộng ngày công', title)
            j = 1

            if obj.month == '2':
                for i in range(3, 31):
                    sheet.set_column('AF:AH', options={'hidden': True})
                    sheet.write(3, i, j, title)
                    sheet.write(4, i, self.getDay(obj.year_id.name, obj.month, j), title)
                    j +=1
            elif obj.month == '2' and checkYear(obj.year_id.name):
                for i in range(3,32):
                    sheet.set_column('AG:AH', options={'hidden': True})
                    sheet.write(3, i, j, title)
                    sheet.write(4, i, self.getDay(obj.year_id.name, obj.month, j), title)
                    j+=1
            elif obj.month in ['2','4','6','9','11']:
                for i in range(3,33):
                    sheet.set_column('AH:AH', options={'hidden': True})
                    sheet.write(3, i, j, title)
                    sheet.write(4, i, self.getDay(obj.year_id.name, obj.month, j), title)
                    j+=1
            else:
                for i in range(3,34):
                    sheet.write(3, i, j, title)
                    sheet.write(4, i, self.getDay(obj.year_id.name, obj.month, j), title)
                    j+=1

            # Xuất ngày công
            content = workbook.add_format({'font_size': 12, 'align': 'center','bold': False, 'border': 1, 'font_color': 'black', 'font_name': 'Times New Roman'})
            k = 5
            no = 1
            for rec in obj.attendance_ids:
                sheet.write(k, 0, no, content)
                sheet.write(k, 1, rec.name.name, content)
                sheet.write(k, 2, rec.position, content)
                # if rec.one.name == False:
                #     sheet.write(k, 3, '+', content)
                #     rec.percentage +=1
                # else:
                sheet.write(k, 3, rec.one.name, content)

                # if rec.two.name == False:
                #     sheet.write(k, 4, "+", content)
                #     rec.percentage +=1
                # else:
                sheet.write(k, 4, rec.two.name, content)

                sheet.write(k, 5, rec.three.name, content)
                sheet.write(k, 6, rec.four.name, content)
                sheet.write(k, 7, rec.five.name, content)
                sheet.write(k, 8, rec.six.name, content)
                sheet.write(k, 9, rec.seven.name, content)
                sheet.write(k, 10, rec.eight.name, content)
                sheet.write(k, 11, rec.nine.name, content)
                sheet.write(k, 12, rec.ten.name, content)

                sheet.write(k, 13, rec.one_1.name, content)
                sheet.write(k, 14, rec.one_2.name, content)
                sheet.write(k, 15, rec.one_3.name, content)
                sheet.write(k, 16, rec.one_4.name, content)
                sheet.write(k, 17, rec.one_5.name, content)
                sheet.write(k, 18, rec.one_6.name, content)
                sheet.write(k, 19, rec.one_7.name, content)
                sheet.write(k, 20, rec.one_8.name, content)
                sheet.write(k, 21, rec.one_9.name, content)
                sheet.write(k, 22, rec.one_0.name, content)

                sheet.write(k, 23, rec.two_1.name, content)
                sheet.write(k, 24, rec.two_2.name, content)
                sheet.write(k, 25, rec.two_3.name, content)
                sheet.write(k, 26, rec.two_4.name, content)
                sheet.write(k, 27, rec.two_5.name, content)
                sheet.write(k, 28, rec.two_6.name, content)
                sheet.write(k, 29, rec.two_7.name, content)
                sheet.write(k, 30, rec.two_8.name, content)
                sheet.write(k, 31, rec.two_9.name, content)
                sheet.write(k, 32, rec.two_0.name, content)
                sheet.write(k, 33, rec.three_1.name, content)
                sheet.write(k, 34, rec.percentage, content)
                k+=1
                no+=1

            # footer

            title2 = workbook.add_format({'font_size': 12, 'align': 'center','bold': True, 'font_color': 'black', 'font_name': 'Times New Roman'})
            content2 = workbook.add_format({'font_size': 12, 'align': 'left','bold': False, 'font_color': 'black', 'font_name': 'Times New Roman'})
            content3 = workbook.add_format({'font_size': 12, 'align': 'center','bold': False, 'italic': True, 'font_color': 'black', 'font_name': 'Times New Roman'})

            sheet.write(17, 1, "Kí hiệu chấm công:", title2)
            sheet.write(18, 1, "- Ốm, điều dưỡng:", content2)
            sheet.write(19, 1, "- Con ốm:", content2)
            sheet.write(20, 1, "- Thai sản:", content2)
            sheet.write(21, 1, "- Tai nạn:", content2)
            sheet.write(22, 1, "- Chủ nhật", content2)
            sheet.write(23, 1, "- Nghỉ lễ", content2)

            sheet.write(18, 2, "Ô", content2)
            sheet.write(19, 2, "Cô", content2)
            sheet.write(20, 2, "TS", content2)
            sheet.write(21, 2, "T", content2)
            sheet.write(22, 2, "CN", content2)
            sheet.write(23, 2, "NL", content2)

            sheet.merge_range('E19:G19', '- Nghỉ nửa ngày không lương:', content2)
            sheet.merge_range('E20:G20', '- Nghỉ không lương:', content2)
            sheet.merge_range('E21:G21', '- Ngừng việc:', content2)
            sheet.merge_range('E22:G22', '- Nghỉ phép:', content2)
            sheet.merge_range('E23:G23', '- Nghỉ nửa ngày tính phép', content2)
            sheet.merge_range('E24:G24', '- Làm cả ngày :', content2)

            sheet.write(18, 7, "-", content2)
            sheet.write(19, 7, "0", content2)
            sheet.write(20, 7, "N", content2)
            sheet.write(21, 7, "P", content2)
            sheet.write(22, 7, "1/2P", content2)
            sheet.write(23, 7, "+", content2)

            sheet.merge_range('Z19:AC19', 'Thái Ngyên, ngày       tháng '+str(obj.month)+' năm '+str(obj.year_id.name), title2)
            sheet.merge_range('V20:Z20', 'Người chấm công', title2)
            sheet.merge_range('V21:Z21', '(Ký, họ tên)', content3)
            sheet.merge_range('AC20:AG20', 'Giám đốc', title2)
            sheet.merge_range('AC21:AG21', '(Ký, họ tên)', content3)
            # sheet.write(0, 0, obj.name, bold)
            # sheet.write(0, 1, obj.month_id.name, bold)