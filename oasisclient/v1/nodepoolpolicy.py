from oasisclient.common import base
from oasisclient.common import utils
import jsonpatch
import json

class NodePoolPolicy(base.Resource):
    def __repr__(self):
        return "<NodePool %s>" % self._info


class NodePoolPolicyManager(base.Manager):
    resource_class = NodePoolPolicy

    @staticmethod
    def _path(id=None):
        return '/v1/nodepool_policies/%s' % id if id else '/v1/nodepool_policies'

    def list(self, limit=None, marker=None, sort_key=None,
             sort_dir=None, detail=False):
        """Retrieve a list of bays.
        :param marker: Optional, the UUID of a bay, eg the last
                       bay from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of bays to return.
            2) limit == 0, return the entire list of bays.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Magnum API
               (see Magnum's api.max_limit option).

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param detail: Optional, boolean whether to return detailed information
                       about bays.

        :returns: A list of bays.
        """
        if limit is not None:
            limit = int(limit)

        filters = utils.common_filters(marker, limit, sort_key, sort_dir)

        path = ''
        if detail:
            path += 'detail'
        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "nodepool_policies")
        else:
            return self._list_pagination(self._path(path), "nodepool_policies", limit=limit)

    def create(self, **param):
        return self._create(self._path(), param)

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None

    def update(self, id, **param):
        original_policy = self.get(id).to_dict()
        del original_policy['created_at']
        del original_policy['updated_at']
        del original_policy['id']
        del original_policy['project_id']
        del original_policy['user_id']
        patch = jsonpatch.JsonPatch.from_diff(original_policy, param)
        return self._update(self._path(id), json.loads(str(patch)))

    def delete(self, id):
        return self._delete(self._path(id))

    def test(self):
        try:
            return self._test('/')
        except Exception :
            return 'Test Connect Error'
