
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

    name = fields.Char('Description', readonly=True)
    standard_id = fields.Many2one('school.standard', 'Academic Class',
                                  required=True,
                                  help="Select Standard")
    month_id = fields.Many2one('academic.month', 'Month', required=True,
                               help="Select Academic Month")
    year_id = fields.Many2one('academic.year', 'Year', required=True)
    attendance_ids = fields.One2many('attendance.sheet.line', 'standard_id',
                                     'Attendance',
                                     help="Academic Year")
    user_id = fields.Many2one('school.teacher', 'Faculty',
                              help="Select Teacher")
    attendance_type = fields.Selection([('daily', 'FullDay'),
                                        ('lecture', 'Lecture Wise')], 'Type')

    @api.onchange('standard_id')
    def onchange_class_info(self):
        '''Method to get student roll no'''
        stud_list = []
        stud_obj = self.env['student.student']
        for rec in self:
            if rec.standard_id:
                stud_list = [{'roll_no': stu.roll_no, 'name': stu.name}
                             for stu in stud_obj.search([('standard_id', '=',
                                                          rec.standard_id),
                                                         ('state', '=',
                                                          'done')])]
            rec.attendance_ids = stud_list

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
        if view_type == 'form':
            digits_temp_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four',
                                5: 'five', 6: 'six', 7: 'seven', 8: 'eight',
                                9: 'nine', 10: 'ten', 11: 'one_1', 12: 'one_2',
                                13: 'one_3', 14: 'one_4', 15: 'one_5',
                                16: 'one_6', 17: 'one_7', 18: 'one_8',
                                19: 'one_9', 20: 'one_0',
                                21: 'two_1', 22: 'two_2', 23: 'two_3',
                                24: 'two_4', 25: 'two_5',
                                26: 'two_6', 27: 'two_7', 28: 'two_8',
                                29: 'two_9', 30: 'two_0',
                                31: 'three_1'}
            flag = 1
            if st_dates and end_dates:
                while st_dates <= end_dates:
                    res['fields']['attendance_ids'
                                  ]['views'
                                    ]['tree'
                                      ]['fields'
                                        ][digits_temp_dict.get(flag)
                                          ]['string'
                                            ] = st_dates.day
                    st_dates += rd(days=1)
                    flag += 1
            if flag < 32:
                res['fields']['attendance_ids'
                              ]['views']['tree'
                                         ]['fields'
                                           ][digits_temp_dict.get(flag)
                                             ]['string'] = ''
                doc2 = etree.XML(res['fields']['attendance_ids']['views'
                                                                 ]['tree'
                                                                   ]['arch'])
                nodes = doc2.xpath("//field[@name='" +
                                   digits_temp_dict.get(flag) + "']")
                for node in nodes:
                    node.set('modifiers', json.dumps({'invisible': True}))
                res['fields']['attendance_ids'
                              ]['views']['tree']['arch'] = etree.tostring(doc2)
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

    roll_no = fields.Integer('Roll Number', required=True,
                             help='Roll Number of Student')
    standard_id = fields.Many2one('attendance.sheet', 'Standard')
    name = fields.Char('Student Name', required=True, readonly=True)
    one = fields.Boolean('1')
    two = fields.Boolean('2')
    three = fields.Boolean('3')
    four = fields.Boolean('4')
    five = fields.Boolean('5')
    seven = fields.Boolean('7')
    six = fields.Boolean('6')
    eight = fields.Boolean('8')
    nine = fields.Boolean('9')
    ten = fields.Boolean('10')
    one_1 = fields.Boolean('11')
    one_2 = fields.Boolean('12')
    one_3 = fields.Boolean('13')
    one_4 = fields.Boolean('14')
    one_5 = fields.Boolean('15')
    one_6 = fields.Boolean('16')
    one_7 = fields.Boolean('17')
    one_8 = fields.Boolean('18')
    one_9 = fields.Boolean('19')
    one_0 = fields.Boolean('20')
    two_1 = fields.Boolean('21')
    two_2 = fields.Boolean('22')
    two_3 = fields.Boolean('23')
    two_4 = fields.Boolean('24')
    two_5 = fields.Boolean('25')
    two_6 = fields.Boolean('26')
    two_7 = fields.Boolean('27')
    two_8 = fields.Boolean('28')
    two_9 = fields.Boolean('29')
    two_0 = fields.Boolean('30')
    three_1 = fields.Boolean('31')
    percentage = fields.Float(compute="_compute_percentage", method=True,
                              string='Attendance (%)', store=False)
