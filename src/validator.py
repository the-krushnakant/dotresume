import yaml
import re
from .utils import is_valid_date


class YAMLResumeValidator:
    def __init__(self, yaml_data):
        self.data = yaml_data

    def validate(self):
        errors = []
        errors.extend(self.validate_personal_info())
        errors.extend(self.validate_contact())
        errors.extend(self.validate_education())
        errors.extend(self.validate_experience())
        errors.extend(self.validate_projects())
        errors.extend(self.validate_skills())
        errors.extend(self.validate_additional_info())
        return errors

    def validate_personal_info(self):
        errors = []
        if not isinstance(self.data.get('name'), str):
            errors.append("'name' must be a string")
        if 'preferred_name' in self.data and not isinstance(self.data['preferred_name'], str):
            errors.append("'preferred_name' must be a string")
        return errors

    def validate_contact(self):
        errors = []
        contact = self.data.get('contact', {})
        if not isinstance(contact, dict):
            return ["'contact' must be a dictionary"]

        if not isinstance(contact.get('email'), str) or not re.match(r"[^@]+@[^@]+\.[^@]+", contact.get('email', '')):
            errors.append("Invalid email format")
        if not isinstance(contact.get('phone'), str):
            errors.append("'phone' must be a string")
        if 'linkedin' in contact and not isinstance(contact['linkedin'], str):
            errors.append("'linkedin' must be a string")
        if 'website' in contact and not isinstance(contact['website'], str):
            errors.append("'website' must be a string")
        if 'github' in contact and not isinstance(contact['github'], str):
            errors.append("'github' must be a string")
        return errors

    def validate_education(self):
        errors = []
        education = self.data.get('education', [])
        if not isinstance(education, list):
            return ["'education' must be a list"]

        for idx, edu in enumerate(education):
            if not isinstance(edu, dict):
                errors.append(f"Education entry {idx} must be a dictionary")
                continue
            if not isinstance(edu.get('institution'), str):
                errors.append(f"Education entry {idx}: 'institution' must be a string")
            if not isinstance(edu.get('degree'), str):
                errors.append(f"Education entry {idx}: 'degree' must be a string")
            if not isinstance(edu.get('dates'), dict):
                errors.append(f"Education entry {idx}: 'dates' must be a dictionary")
            else:
                if not is_valid_date(edu['dates'].get('start')):
                    errors.append(f"Education entry {idx}: Invalid start date")
                if not is_valid_date(edu['dates'].get('graduation')):
                    errors.append(f"Education entry {idx}: Invalid graduation date")
            if 'gpa' in edu:
                if not isinstance(edu['gpa'], dict):
                    errors.append(f"Education entry {idx}: 'gpa' must be a dictionary")
                else:
                    if not isinstance(edu['gpa'].get('value'), (int, float)):
                        errors.append(f"Education entry {idx}: GPA value must be a number")
                    if not isinstance(edu['gpa'].get('scale'), (int, float)):
                        errors.append(f"Education entry {idx}: GPA scale must be a number")
        return errors

    def validate_experience(self):
        errors = []
        experience = self.data.get('experience', [])
        if not isinstance(experience, list):
            return ["'experience' must be a list"]

        for idx, exp in enumerate(experience):
            if not isinstance(exp, dict):
                errors.append(f"Experience entry {idx} must be a dictionary")
                continue
            if not isinstance(exp.get('company'), str):
                errors.append(f"Experience entry {idx}: 'company' must be a string")
            if not isinstance(exp.get('position'), str):
                errors.append(f"Experience entry {idx}: 'position' must be a string")
            if not isinstance(exp.get('dates'), dict):
                errors.append(f"Experience entry {idx}: 'dates' must be a dictionary")
            else:
                if not is_valid_date(exp['dates'].get('start')):
                    errors.append(f"Experience entry {idx}: Invalid start date")
                if exp['dates'].get('end') != 'Present' and not is_valid_date(exp['dates'].get('end')):
                    errors.append(f"Experience entry {idx}: Invalid end date")
            if not isinstance(exp.get('responsibilities'), list):
                errors.append(f"Experience entry {idx}: 'responsibilities' must be a list")
            else:
                for resp in exp['responsibilities']:
                    if not isinstance(resp, str):
                        errors.append(f"Experience entry {idx}: Each responsibility must be a string")
        return errors

    def validate_projects(self):
        errors = []
        projects = self.data.get('projects', [])
        if not isinstance(projects, list):
            return ["'projects' must be a list"]

        for idx, proj in enumerate(projects):
            if not isinstance(proj, dict):
                errors.append(f"Project entry {idx} must be a dictionary")
                continue
            if not isinstance(proj.get('name'), str):
                errors.append(f"Project entry {idx}: 'name' must be a string")
            if not isinstance(proj.get('description'), str):
                errors.append(f"Project entry {idx}: 'description' must be a string")
            if not isinstance(proj.get('technologies'), list):
                errors.append(f"Project entry {idx}: 'technologies' must be a list")
            else:
                for tech in proj['technologies']:
                    if not isinstance(tech, str):
                        errors.append(f"Project entry {idx}: Each technology must be a string")
        return errors

    def validate_skills(self):
        errors = []
        skills = self.data.get('skills', [])
        if not isinstance(skills, list):
            return ["'skills' must be a list"]
        for skill in skills:
            if not isinstance(skill, str):
                errors.append("Each skill must be a string")
        return errors

    def validate_additional_info(self):
        errors = []
        additional_info = self.data.get('additional_info', {})
        if not isinstance(additional_info, dict):
            return ["'additional_info' must be a dictionary"]

        us_specific = additional_info.get('us_specific', {})
        if not isinstance(us_specific, dict):
            errors.append("'us_specific' must be a dictionary")
        else:
            if not isinstance(us_specific.get('veteran_status'), str):
                errors.append("'veteran_status' must be a string")
            if not isinstance(us_specific.get('disability_status'), str):
                errors.append("'disability_status' must be a string")
            diversity_info = us_specific.get('diversity_info', {})
            if not isinstance(diversity_info, dict):
                errors.append("'diversity_info' must be a dictionary")
            else:
                if not isinstance(diversity_info.get('ethnicity'), str):
                    errors.append("'ethnicity' must be a string")
                if not isinstance(diversity_info.get('gender'), str):
                    errors.append("'gender' must be a string")
        return errors

    @staticmethod
    def check(yaml_string):
        try:
            yaml_data = yaml.safe_load(yaml_string)
            validator = YAMLResumeValidator(yaml_data)
            errors = validator.validate()
            if errors:
                return False, errors
            return True, []
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML: {str(e)}"]


