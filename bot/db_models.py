from datetime import datetime
import uuid
import traceback

from pynamodb.attributes import JSONAttribute, UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model

from bot.config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY


class SchedulerConfig(Model):
    class Meta:
        aws_access_key_id = AWS_ACCESS_KEY_ID
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        table_name = "craimer_scheduler_config"
        region = AWS_REGION

    can_create = "can_create_scheduler_config"
    can_update = "can_update_scheduler_config"
    can_delete = "can_delete_scheduler_config"
    can_get = "can_get_scheduler_config"

    user_id = UnicodeAttribute(hash_key=True)
    scheduler_id = UnicodeAttribute(range_key=True, default=lambda: str(uuid.uuid4()))

    name = UnicodeAttribute(null=True)
    location = UnicodeAttribute(null=True)
    filters = JSONAttribute(null=True)
    mapping = JSONAttribute(null=True)
    service_name = UnicodeAttribute(null=True)

    created_at = UTCDateTimeAttribute(default=datetime.utcnow)
    updated_at = UTCDateTimeAttribute(null=True, default=datetime.utcnow)

    def serializer(self):
        return {
            "user_id": self.user_id,
            "scheduler_id": self.scheduler_id,
            "name": self.name,
            "location": self.location,
            "filters": self.filters,
            # "mapping": self.mapping,
            "service_name": self.service_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def get_all_by_user(user_id: str):
        try:
            return list(SchedulerConfig.query(user_id))
        except Exception:
            traceback.print_exc()
            return []

    @staticmethod
    def get_one(user_id: str, scheduler_id: str):
        try:
            return SchedulerConfig.get(user_id, range_key=scheduler_id)
        except SchedulerConfig.DoesNotExist:
            return None
        except Exception:
            traceback.print_exc()
            return None

    def update_config(self, data):
        try:
            updates = []
            if "name" in data and data["name"] is not None:
                updates.append(SchedulerConfig.name.set(data["name"]))
            if "location" in data and data["location"] is not None:
                updates.append(SchedulerConfig.location.set(data["location"]))
            if "filters" in data and data["filters"] is not None:
                updates.append(SchedulerConfig.filters.set(data["filters"]))
            if "mapping" in data and data["mapping"] is not None:
                updates.append(SchedulerConfig.mapping.set(data["mapping"]))
            if "service_name" in data and data["service_name"] is not None:
                updates.append(SchedulerConfig.service_name.set(data["service_name"]))

            updates.append(SchedulerConfig.updated_at.set(datetime.utcnow()))

            if updates:
                self.update(actions=updates)
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def delete_config(user_id: str, scheduler_id: str):
        try:
            config = SchedulerConfig.get(user_id, range_key=scheduler_id)
            config.delete()
            return True
        except SchedulerConfig.DoesNotExist:
            return False
        except Exception:
            traceback.print_exc()
            return False


# Create the table if it doesn't exist
def create_table():
    if not SchedulerConfig.exists():
        SchedulerConfig.create_table(wait=True)