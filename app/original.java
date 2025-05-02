public class MaxSubarrayTree {
    static class Node {
        long sum, bestPrefix, bestSuffix, bestSum;
        Node(long v) {
            sum = bestPrefix = bestSuffix = bestSum = v;
        }
        Node() {
            sum = bestPrefix = bestSuffix = bestSum = Long.MIN_VALUE;
        }
    }

    public static void build(int idx, int left, int right) {
        if (left == right) {
            segTree[idx] = new Node(arr[left]);
        } else {
            int mid = (left + right) >>> 1;
            build(idx<<1, left, mid);
            build(idx<<1|1, mid+1, right);
            segTree[idx] = merge(segTree[idx<<1], segTree[idx<<1|1]);
        }
    }

    private static Node merge(Node L, Node R) {
        Node res = new Node();
        res.sum = L.sum + R.sum;
        res.bestPrefix = Math.max(L.bestPrefix, L.sum + R.bestPrefix);
        res.bestSuffix = Math.max(R.bestSuffix, R.sum + L.bestSuffix);
        res.bestSum = Math.max(Math.max(L.bestSum, R.bestSum), L.bestSuffix + R.bestPrefix);
        return res;
    }

    public static void update(int idx, int left, int right, int pos, long val) {
        if (left == right) {
            segTree[idx] = new Node(val);
        } else {
            int mid = (left + right) >>> 1;
            if (pos <= mid) update(idx<<1, left, mid, pos, val);
            else update(idx<<1|1, mid+1, right, pos, val);
            segTree[idx] = merge(segTree[idx<<1], segTree[idx<<1|1]);
        }
    }
}
